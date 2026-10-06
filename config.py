"""
Configuration for Multi-Agent Gemma System
"""

# Model Configuration
MODEL_NAME = "google/gemma-2b-it"  # Using Gemma 2B for faster inference
# Alternative: "google/gemma-7b-it" for better quality

# Role Definitions
ROLES = {
    "expert": {
        "name": "Domain Expert",
        "system_prompt": """You are a highly knowledgeable domain expert with years of experience.
Analyze the given problem deeply using your expertise. Provide detailed, technical insights.
Focus on accuracy and depth of understanding. Cite specific knowledge when applicable.""",
        "temperature": 0.3,
        "weight": 0.35
    },
    "skeptic": {
        "name": "Critical Skeptic",
        "system_prompt": """You are a critical skeptic who questions assumptions and looks for flaws.
Your job is to identify potential errors, biases, or overlooked issues in the analysis.
Challenge questionable claims and demand evidence. Point out ambiguities and edge cases.""",
        "temperature": 0.5,
        "weight": 0.25
    },
    "beginner": {
        "name": "Curious Beginner",
        "system_prompt": """You are a curious beginner trying to understand the problem clearly.
Ask clarifying questions and check if explanations make sense to someone learning.
Identify jargon that needs explanation. Ensure the reasoning is logically sound and accessible.""",
        "temperature": 0.6,
        "weight": 0.15
    },
    "verifier": {
        "name": "Fact Verifier",
        "system_prompt": """You are a meticulous fact-checker and verifier.
Cross-check information for consistency and accuracy. Look for contradictions.
Validate claims against known facts. Assess confidence levels in conclusions.""",
        "temperature": 0.2,
        "weight": 0.25
    }
}

# Reconciliation Configuration
RECONCILIATION_METHOD = "weighted_voting"  # Options: "simple_voting", "weighted_voting", "consensus"
CONFIDENCE_THRESHOLD = 0.6
MIN_AGREEMENT_THRESHOLD = 0.5

# Evaluation Configuration
TEST_DOMAINS = ["medical", "code_review", "math", "fact_checking", "image_analysis"]
EVALUATION_METRICS = ["accuracy", "precision", "recall", "f1_score", "response_time"]

# UI Configuration
STREAMLIT_THEME = "light"
SHOW_INTERMEDIATE_OUTPUTS = True
ENABLE_VISUALIZATION = True
