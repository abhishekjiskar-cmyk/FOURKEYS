"""
Evaluation script to compare single-agent vs multi-agent performance
"""
import json
import time
from typing import Dict, List
import numpy as np
from agents import MultiAgentSystem, SingleAgentBaseline
from reconciliation import Reconciler, analyze_disagreements
from test_dataset import TEST_CASES, get_all_domains
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Evaluator:
    """Evaluates and compares single vs multi-agent approaches"""

    def __init__(self, use_api: bool = False):
        """
        Initialize evaluator

        Args:
            use_api: Whether to use API or local models
        """
        self.multi_agent = MultiAgentSystem(use_api=use_api)
        self.single_agent = SingleAgentBaseline(use_api=use_api)
        self.reconciler = Reconciler()

    def evaluate_response(self, response: str, ground_truth: str, keywords: List[str]) -> Dict:
        """
        Evaluate a response against ground truth

        Args:
            response: Generated response
            ground_truth: Expected answer
            keywords: Keywords that should appear

        Returns:
            Evaluation metrics
        """
        response_lower = response.lower()
        ground_truth_lower = ground_truth.lower()

        # Keyword matching
        keywords_found = sum(1 for kw in keywords if kw.lower() in response_lower)
        keyword_score = keywords_found / len(keywords) if keywords else 0

        # Simple semantic similarity (word overlap)
        response_words = set(response_lower.split())
        truth_words = set(ground_truth_lower.split())

        if not truth_words:
            semantic_score = 0
        else:
            intersection = response_words.intersection(truth_words)
            semantic_score = len(intersection) / len(truth_words)

        # Combined score
        overall_score = (keyword_score * 0.6 + semantic_score * 0.4)

        return {
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "overall_score": overall_score,
            "keywords_found": keywords_found,
            "total_keywords": len(keywords)
        }

    def run_single_test(self, test_case: Dict) -> Dict:
        """
        Run single test case with both approaches

        Args:
            test_case: Test case dict

        Returns:
            Results for both approaches
        """
        problem = test_case["problem"]
        ground_truth = test_case["ground_truth"]
        keywords = test_case["keywords"]

        print(f"\n{'='*60}")
        print(f"Test ID: {test_case['id']} | Domain: {test_case['domain']}")
        print(f"Problem: {problem[:100]}...")

        # Single agent
        print("\n[Single Agent]")
        single_start = time.time()
        single_response = self.single_agent.analyze(problem)
        single_time = time.time() - single_start

        single_eval = self.evaluate_response(
            single_response["response"],
            ground_truth,
            keywords
        )

        print(f"Time: {single_time:.2f}s | Score: {single_eval['overall_score']:.2f}")

        # Multi-agent
        print("\n[Multi-Agent System]")
        multi_start = time.time()
        perspectives = self.multi_agent.get_perspectives(problem, parallel=True)
        reconciled = self.reconciler.reconcile(perspectives)
        multi_time = time.time() - multi_start

        multi_eval = self.evaluate_response(
            reconciled["final_answer"],
            ground_truth,
            keywords
        )

        print(f"Time: {multi_time:.2f}s | Score: {multi_eval['overall_score']:.2f}")
        print(f"Agreement Level: {reconciled['agreement_level']:.2f}")

        # Analyze disagreements
        disagreement_analysis = analyze_disagreements(perspectives)

        return {
            "test_id": test_case["id"],
            "domain": test_case["domain"],
            "difficulty": test_case["difficulty"],
            "single_agent": {
                "response": single_response["response"],
                "time": single_time,
                "evaluation": single_eval
            },
            "multi_agent": {
                "perspectives": perspectives,
                "reconciled": reconciled,
                "time": multi_time,
                "evaluation": multi_eval,
                "disagreements": disagreement_analysis
            },
            "improvement": multi_eval["overall_score"] - single_eval["overall_score"]
        }

    def run_full_evaluation(self, test_cases: List[Dict] = None) -> Dict:
        """
        Run evaluation on all test cases

        Args:
            test_cases: List of test cases (defaults to all)

        Returns:
            Complete evaluation results
        """
        if test_cases is None:
            test_cases = TEST_CASES

        results = []

        print(f"\n{'#'*60}")
        print(f"Starting Evaluation: {len(test_cases)} test cases")
        print(f"{'#'*60}")

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}/{len(test_cases)} ---")
            try:
                result = self.run_single_test(test_case)
                results.append(result)
            except Exception as e:
                print(f"Error on test {test_case['id']}: {e}")
                continue

        # Aggregate statistics
        stats = self.calculate_statistics(results)

        return {
            "results": results,
            "statistics": stats,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def calculate_statistics(self, results: List[Dict]) -> Dict:
        """Calculate aggregate statistics from results"""

        single_scores = [r["single_agent"]["evaluation"]["overall_score"] for r in results]
        multi_scores = [r["multi_agent"]["evaluation"]["overall_score"] for r in results]
        improvements = [r["improvement"] for r in results]

        # By domain
        domains = set(r["domain"] for r in results)
        domain_stats = {}

        for domain in domains:
            domain_results = [r for r in results if r["domain"] == domain]
            domain_single = [r["single_agent"]["evaluation"]["overall_score"] for r in domain_results]
            domain_multi = [r["multi_agent"]["evaluation"]["overall_score"] for r in domain_results]

            domain_stats[domain] = {
                "count": len(domain_results),
                "single_avg": np.mean(domain_single),
                "multi_avg": np.mean(domain_multi),
                "improvement": np.mean(domain_multi) - np.mean(domain_single)
            }

        # By difficulty
        difficulties = set(r["difficulty"] for r in results)
        difficulty_stats = {}

        for diff in difficulties:
            diff_results = [r for r in results if r["difficulty"] == diff]
            diff_single = [r["single_agent"]["evaluation"]["overall_score"] for r in diff_results]
            diff_multi = [r["multi_agent"]["evaluation"]["overall_score"] for r in diff_results]

            difficulty_stats[diff] = {
                "count": len(diff_results),
                "single_avg": np.mean(diff_single),
                "multi_avg": np.mean(diff_multi),
                "improvement": np.mean(diff_multi) - np.mean(diff_single)
            }

        # Time analysis
        single_times = [r["single_agent"]["time"] for r in results]
        multi_times = [r["multi_agent"]["time"] for r in results]

        return {
            "overall": {
                "total_tests": len(results),
                "single_agent_avg": np.mean(single_scores),
                "multi_agent_avg": np.mean(multi_scores),
                "avg_improvement": np.mean(improvements),
                "improvement_percentage": (np.mean(improvements) / np.mean(single_scores)) * 100,
                "multi_agent_wins": sum(1 for imp in improvements if imp > 0),
                "single_agent_wins": sum(1 for imp in improvements if imp < 0),
                "ties": sum(1 for imp in improvements if imp == 0)
            },
            "by_domain": domain_stats,
            "by_difficulty": difficulty_stats,
            "timing": {
                "single_agent_avg_time": np.mean(single_times),
                "multi_agent_avg_time": np.mean(multi_times),
                "time_overhead": np.mean(multi_times) - np.mean(single_times)
            }
        }

    def generate_visualizations(self, results: Dict, output_dir: str = "./results"):
        """Generate visualization charts"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        stats = results["statistics"]

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)

        # 1. Overall Comparison Bar Chart
        fig, ax = plt.subplots()
        methods = ['Single Agent', 'Multi-Agent']
        scores = [
            stats["overall"]["single_agent_avg"],
            stats["overall"]["multi_agent_avg"]
        ]

        bars = ax.bar(methods, scores, color=['#3498db', '#2ecc71'])
        ax.set_ylabel('Average Score')
        ax.set_title('Single Agent vs Multi-Agent System Performance')
        ax.set_ylim([0, 1])

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/overall_comparison.png", dpi=300)
        plt.close()

        # 2. Domain-wise Comparison
        domain_stats = stats["by_domain"]
        domains = list(domain_stats.keys())
        single_scores_domain = [domain_stats[d]["single_avg"] for d in domains]
        multi_scores_domain = [domain_stats[d]["multi_avg"] for d in domains]

        x = np.arange(len(domains))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))
        bars1 = ax.bar(x - width/2, single_scores_domain, width, label='Single Agent', color='#3498db')
        bars2 = ax.bar(x + width/2, multi_scores_domain, width, label='Multi-Agent', color='#2ecc71')

        ax.set_xlabel('Domain')
        ax.set_ylabel('Average Score')
        ax.set_title('Performance by Domain')
        ax.set_xticks(x)
        ax.set_xticklabels(domains, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim([0, 1])

        plt.tight_layout()
        plt.savefig(f"{output_dir}/domain_comparison.png", dpi=300)
        plt.close()

        # 3. Improvement Distribution
        improvements = [r["improvement"] for r in results["results"]]

        fig, ax = plt.subplots()
        ax.hist(improvements, bins=20, color='#9b59b6', edgecolor='black', alpha=0.7)
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='No improvement')
        ax.set_xlabel('Improvement (Multi-Agent - Single Agent)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Performance Improvements')
        ax.legend()

        plt.tight_layout()
        plt.savefig(f"{output_dir}/improvement_distribution.png", dpi=300)
        plt.close()

        # 4. Win/Loss/Tie Pie Chart
        fig, ax = plt.subplots()
        wins = stats["overall"]["multi_agent_wins"]
        losses = stats["overall"]["single_agent_wins"]
        ties = stats["overall"]["ties"]

        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        ax.pie([wins, losses, ties], labels=['Multi-Agent Wins', 'Single Agent Wins', 'Ties'],
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Multi-Agent vs Single Agent: Win Rate')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/win_rate.png", dpi=300)
        plt.close()

        print(f"\n✓ Visualizations saved to {output_dir}/")

    def save_results(self, results: Dict, filename: str = "./results/evaluation_results.json"):
        """Save results to JSON file"""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Make results JSON serializable
        serializable_results = self._make_serializable(results)

        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)

        print(f"\n✓ Results saved to {filename}")

    def _make_serializable(self, obj):
        """Convert numpy types to native Python types"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        else:
            return obj

    def print_summary(self, results: Dict):
        """Print evaluation summary"""
        stats = results["statistics"]

        print(f"\n{'='*60}")
        print("EVALUATION SUMMARY")
        print(f"{'='*60}")

        print(f"\nTotal Tests: {stats['overall']['total_tests']}")
        print(f"\nSingle Agent Avg Score: {stats['overall']['single_agent_avg']:.3f}")
        print(f"Multi-Agent Avg Score:  {stats['overall']['multi_agent_avg']:.3f}")
        print(f"Average Improvement:    {stats['overall']['avg_improvement']:.3f} ({stats['overall']['improvement_percentage']:.1f}%)")

        print(f"\nWin/Loss Record:")
        print(f"  Multi-Agent Wins: {stats['overall']['multi_agent_wins']}")
        print(f"  Single Agent Wins: {stats['overall']['single_agent_wins']}")
        print(f"  Ties: {stats['overall']['ties']}")

        print(f"\nTiming:")
        print(f"  Single Agent Avg: {stats['timing']['single_agent_avg_time']:.2f}s")
        print(f"  Multi-Agent Avg:  {stats['timing']['multi_agent_avg_time']:.2f}s")
        print(f"  Time Overhead:    {stats['timing']['time_overhead']:.2f}s")

        print(f"\nPerformance by Domain:")
        for domain, dstats in stats['by_domain'].items():
            print(f"  {domain:15s}: +{dstats['improvement']:.3f} ({dstats['count']} tests)")

        print(f"\n{'='*60}\n")


def main():
    """Main evaluation function"""
    print("Multi-Agent Gemma Evaluation System")
    print("=" * 60)

    # Ask user whether to use API or local
    use_api = input("\nUse Google Gemini API? (y/n, default=n): ").lower() == 'y'

    if not use_api:
        print("\n⚠ Using LOCAL models - make sure Gemma is downloaded!")
        print("This requires ~5GB GPU memory for Gemma-2B")

    # Initialize evaluator
    print("\nInitializing system...")
    evaluator = Evaluator(use_api=use_api)

    # Run evaluation
    print("\nRunning evaluation...")
    results = evaluator.run_full_evaluation()

    # Print summary
    evaluator.print_summary(results)

    # Save results
    evaluator.save_results(results)

    # Generate visualizations
    print("\nGenerating visualizations...")
    evaluator.generate_visualizations(results)

    print("\n✓ Evaluation complete!")
    print("Check ./results/ folder for outputs")


if __name__ == "__main__":
    main()
