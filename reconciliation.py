"""
Reconciliation logic for combining multiple agent perspectives
"""
import re
from typing import List, Dict, Tuple
from collections import Counter
import numpy as np
from config import RECONCILIATION_METHOD, CONFIDENCE_THRESHOLD, MIN_AGREEMENT_THRESHOLD


class Reconciler:
    """Reconciles multiple agent perspectives into final answer"""

    def __init__(self, method: str = RECONCILIATION_METHOD):
        """
        Initialize reconciler

        Args:
            method: Reconciliation method (simple_voting, weighted_voting, consensus)
        """
        self.method = method

    def reconcile(self, perspectives: List[Dict]) -> Dict:
        """
        Reconcile multiple perspectives into final answer

        Args:
            perspectives: List of agent responses

        Returns:
            Dict with final answer, confidence, and metadata
        """
        if self.method == "simple_voting":
            return self._simple_voting(perspectives)
        elif self.method == "weighted_voting":
            return self._weighted_voting(perspectives)
        elif self.method == "consensus":
            return self._consensus_based(perspectives)
        else:
            raise ValueError(f"Unknown reconciliation method: {self.method}")

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text"""
        # Simple extraction: split by sentences and periods
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _simple_voting(self, perspectives: List[Dict]) -> Dict:
        """
        Simple majority voting

        Args:
            perspectives: Agent responses

        Returns:
            Reconciled answer
        """
        # Compare all pairs of responses
        similarity_matrix = np.zeros((len(perspectives), len(perspectives)))

        for i in range(len(perspectives)):
            for j in range(i+1, len(perspectives)):
                sim = self._calculate_similarity(
                    perspectives[i]["response"],
                    perspectives[j]["response"]
                )
                similarity_matrix[i][j] = sim
                similarity_matrix[j][i] = sim

        # Find response with highest average similarity
        avg_similarities = similarity_matrix.mean(axis=1)
        best_idx = int(np.argmax(avg_similarities))

        return {
            "final_answer": perspectives[best_idx]["response"],
            "confidence": float(avg_similarities[best_idx]),
            "method": "simple_voting",
            "agreement_level": float(avg_similarities.mean()),
            "selected_role": perspectives[best_idx]["role_name"],
            "all_agreed": avg_similarities.min() > MIN_AGREEMENT_THRESHOLD
        }

    def _weighted_voting(self, perspectives: List[Dict]) -> Dict:
        """
        Weighted voting based on role weights

        Args:
            perspectives: Agent responses

        Returns:
            Reconciled answer with weights considered
        """
        # Calculate weighted similarities
        total_weight = sum(p["weight"] for p in perspectives)

        weighted_scores = []
        for i, perspective in enumerate(perspectives):
            score = 0
            for j, other in enumerate(perspectives):
                if i != j:
                    sim = self._calculate_similarity(
                        perspective["response"],
                        other["response"]
                    )
                    score += sim * other["weight"]

            # Normalize by total weight
            weighted_scores.append(score / total_weight)

        # Select response with highest weighted score
        best_idx = int(np.argmax(weighted_scores))

        # Build comprehensive answer
        final_answer = self._build_comprehensive_answer(perspectives, best_idx)

        return {
            "final_answer": final_answer,
            "confidence": float(weighted_scores[best_idx]),
            "method": "weighted_voting",
            "agreement_level": float(np.mean(weighted_scores)),
            "selected_role": perspectives[best_idx]["role_name"],
            "all_agreed": min(weighted_scores) > MIN_AGREEMENT_THRESHOLD,
            "role_contributions": {
                p["role_name"]: float(weighted_scores[i])
                for i, p in enumerate(perspectives)
            }
        }

    def _consensus_based(self, perspectives: List[Dict]) -> Dict:
        """
        Build consensus from all perspectives

        Args:
            perspectives: Agent responses

        Returns:
            Synthesized consensus answer
        """
        # Extract all key points
        all_points = []
        for p in perspectives:
            points = self._extract_key_points(p["response"])
            for point in points:
                all_points.append({
                    "text": point,
                    "role": p["role_name"],
                    "weight": p["weight"]
                })

        # Group similar points
        point_groups = []
        used = set()

        for i, point in enumerate(all_points):
            if i in used:
                continue

            group = [point]
            group_weight = point["weight"]

            for j, other_point in enumerate(all_points):
                if i != j and j not in used:
                    sim = self._calculate_similarity(point["text"], other_point["text"])
                    if sim > 0.5:  # Similar points
                        group.append(other_point)
                        group_weight += other_point["weight"]
                        used.add(j)

            point_groups.append({
                "points": group,
                "total_weight": group_weight,
                "count": len(group)
            })
            used.add(i)

        # Sort by weight and count
        point_groups.sort(key=lambda x: (x["total_weight"], x["count"]), reverse=True)

        # Build consensus answer from top groups
        consensus_parts = []
        for group in point_groups[:3]:  # Top 3 most agreed points
            # Use the point from the highest-weighted role in the group
            best_point = max(group["points"], key=lambda x: x["weight"])
            consensus_parts.append(best_point["text"])

        consensus_answer = " ".join(consensus_parts)

        return {
            "final_answer": consensus_answer,
            "confidence": float(point_groups[0]["total_weight"] / sum(p["weight"] for p in perspectives)),
            "method": "consensus",
            "agreement_level": float(len([g for g in point_groups if g["count"] > 2]) / len(point_groups)),
            "num_consensus_points": len(point_groups),
            "all_agreed": len([g for g in point_groups if g["count"] == len(perspectives)]) > 0
        }

    def _build_comprehensive_answer(self, perspectives: List[Dict], primary_idx: int) -> str:
        """
        Build comprehensive answer using primary perspective and key insights from others

        Args:
            perspectives: All perspectives
            primary_idx: Index of primary/best perspective

        Returns:
            Comprehensive answer
        """
        primary = perspectives[primary_idx]
        answer_parts = [f"**Primary Analysis ({primary['role_name']}):**\n{primary['response']}"]

        # Add unique insights from other roles
        for i, p in enumerate(perspectives):
            if i != primary_idx:
                # Check if this perspective adds unique value
                sim = self._calculate_similarity(primary["response"], p["response"])
                if sim < 0.7:  # Different enough to include
                    answer_parts.append(f"\n**Additional Perspective ({p['role_name']}):**\n{p['response']}")

        return "\n".join(answer_parts)


def analyze_disagreements(perspectives: List[Dict]) -> Dict:
    """
    Analyze where and why agents disagree

    Args:
        perspectives: List of agent responses

    Returns:
        Disagreement analysis
    """
    reconciler = Reconciler()

    # Calculate pairwise similarities
    disagreements = []

    for i in range(len(perspectives)):
        for j in range(i+1, len(perspectives)):
            sim = reconciler._calculate_similarity(
                perspectives[i]["response"],
                perspectives[j]["response"]
            )

            if sim < 0.5:  # Significant disagreement
                disagreements.append({
                    "role1": perspectives[i]["role_name"],
                    "role2": perspectives[j]["role_name"],
                    "similarity": sim,
                    "response1": perspectives[i]["response"][:200] + "...",
                    "response2": perspectives[j]["response"][:200] + "..."
                })

    return {
        "num_disagreements": len(disagreements),
        "disagreements": disagreements,
        "has_major_disagreement": len(disagreements) > 0
    }
