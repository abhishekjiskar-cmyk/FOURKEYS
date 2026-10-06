"""
Multi-Agent System Implementation
"""
import time
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import ROLES
from models import ModelPool

class Agent:
    """Individual agent with specific role"""

    def __init__(self, role: str, model_pool: ModelPool):
        """
        Initialize agent with role

        Args:
            role: Role name (expert, skeptic, beginner, verifier)
            model_pool: Shared model pool
        """
        self.role = role
        self.config = ROLES[role]
        self.model_pool = model_pool

    def analyze(self, problem: str, image=None) -> Dict[str, any]:
        """
        Analyze problem from this agent's perspective

        Args:
            problem: Problem statement or question
            image: Optional PIL Image

        Returns:
            Dict with response, confidence, and metadata
        """
        start_time = time.time()

        model = self.model_pool.get_model()

        # Generate response
        response = model.generate(
            prompt=problem,
            system_prompt=self.config["system_prompt"],
            temperature=self.config["temperature"],
            image=image
        )

        inference_time = time.time() - start_time

        return {
            "role": self.role,
            "role_name": self.config["name"],
            "response": response,
            "weight": self.config["weight"],
            "temperature": self.config["temperature"],
            "inference_time": inference_time
        }


class MultiAgentSystem:
    """Orchestrates multiple agents to solve problems"""

    def __init__(self, use_api: bool = False, model_name: str = "google/gemma-2b-it"):
        """
        Initialize multi-agent system

        Args:
            use_api: Whether to use API or local models
            model_name: The HuggingFace model identifier for local inference
        """
        self.model_pool = ModelPool(use_api=use_api, model_name=model_name)
        self.agents = {
            role: Agent(role, self.model_pool)
            for role in ROLES.keys()
        }

    def analyze_parallel(self, problem: str, image=None) -> List[Dict]:
        """
        Get analysis from all agents in parallel

        Args:
            problem: Problem statement
            image: Optional PIL Image

        Returns:
            List of agent responses
        """
        responses = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(agent.analyze, problem, image): role
                for role, agent in self.agents.items()
            }

            for future in as_completed(futures):
                try:
                    response = future.result()
                    responses.append(response)
                except Exception as e:
                    role = futures[future]
                    print(f"Error in {role} agent: {e}")
                    responses.append({
                        "role": role,
                        "role_name": ROLES[role]["name"],
                        "response": f"Error: {str(e)}",
                        "weight": 0,
                        "temperature": 0,
                        "inference_time": 0
                    })

        return responses

    def analyze_sequential(self, problem: str, image=None) -> List[Dict]:
        """
        Get analysis from all agents sequentially (fallback)

        Args:
            problem: Problem statement
            image: Optional PIL Image

        Returns:
            List of agent responses
        """
        responses = []

        for role, agent in self.agents.items():
            try:
                response = agent.analyze(problem, image)
                responses.append(response)
            except Exception as e:
                print(f"Error in {role} agent: {e}")
                responses.append({
                    "role": role,
                    "role_name": ROLES[role]["name"],
                    "response": f"Error: {str(e)}",
                    "weight": 0,
                    "temperature": 0,
                    "inference_time": 0
                })

        return responses

    def get_perspectives(self, problem: str, parallel: bool = True, image=None) -> List[Dict]:
        """
        Get multiple perspectives on a problem

        Args:
            problem: Problem to analyze
            parallel: Whether to run agents in parallel
            image: Optional PIL Image

        Returns:
            List of agent responses
        """
        if parallel:
            return self.analyze_parallel(problem, image)
        else:
            return self.analyze_sequential(problem, image)


class SingleAgentBaseline:
    """Baseline single-agent for comparison"""

    def __init__(self, use_api: bool = False, model_name: str = "google/gemma-2b-it"):
        """Initialize single agent baseline"""
        self.model_pool = ModelPool(use_api=use_api, model_name=model_name)

    def analyze(self, problem: str, image=None) -> Dict:
        """
        Analyze problem with single agent

        Args:
            problem: Problem statement
            image: Optional PIL Image

        Returns:
            Single response dict
        """
        start_time = time.time()

        model = self.model_pool.get_model()

        response = model.generate(
            prompt=problem,
            system_prompt="You are a helpful AI assistant. Analyze the given problem carefully and provide a clear, accurate answer.",
            temperature=0.7,
            image=image
        )

        inference_time = time.time() - start_time

        return {
            "response": response,
            "inference_time": inference_time
        }
