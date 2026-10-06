"""
Model loading and inference utilities for Gemma
"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import google.generativeai as genai
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

class GemmaModel:
    """Wrapper for Gemma model inference"""

    def __init__(self, use_api: bool = False, model_name: str = "google/gemma-2b-it"):
        """
        Initialize Gemma model
        Args:
            use_api: If True, use Google's Gemini API. If False, use local Gemma model
            model_name: The HuggingFace model identifier for local inference
        """
        self.use_api = use_api
        self.model_name = model_name

        if use_api:
            self._init_api()
        else:
            self._init_local()

    def _init_api(self):
        """Initialize Google Gemini API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        print("[OK] Initialized Gemini API")

    def _init_local(self):
        """Initialize local model with quantization"""
        print(f"Loading {self.model_name}...")

        # Quantization config for efficient inference
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=os.getenv("HF_TOKEN")
        )

        # Load model with quantization
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            token=os.getenv("HF_TOKEN")
        )

        print("[OK] Model loaded successfully")

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_length: int = 512, image = None) -> str:
        """
        Generate response from model

        Args:
            prompt: User prompt
            system_prompt: System/role prompt
            temperature: Sampling temperature
            max_length: Maximum response length
            image: Optional PIL Image for multimodal inference

        Returns:
            Generated text
        """
        if self.use_api:
            return self._generate_api(prompt, system_prompt, temperature, image)
        else:
            return self._generate_local(prompt, system_prompt, temperature, max_length)

    def _generate_api(self, prompt: str, system_prompt: str, temperature: float, image = None) -> str:
        """Generate using Gemini API"""
        import time
        from google.api_core.exceptions import ResourceExhausted

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=512,
        )

        contents = [full_prompt]
        if image:
            contents.append(image)

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    contents,
                    generation_config=generation_config
                )
                return response.text
            except ResourceExhausted as e:
                if attempt < max_retries - 1:
                    time.sleep(10)  # Wait 10 seconds per attempt to handle minute-level quotas
                else:
                    raise e
                    raise e

    def _generate_local(self, prompt: str, system_prompt: str, temperature: float, max_length: int) -> str:
        """Generate using local model"""
        # Format prompt with system instruction
        full_prompt = f"<start_of_turn>user\n{system_prompt}\n\n{prompt}<end_of_turn>\n<start_of_turn>model\n"

        # Tokenize
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode and extract response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)

        # Extract only the model's response
        if "<start_of_turn>model" in response:
            response = response.split("<start_of_turn>model")[-1]
        if "<end_of_turn>" in response:
            response = response.split("<end_of_turn>")[0]

        return response.strip()


class ModelPool:
    """Pool of model instances for parallel inference"""

    def __init__(self, use_api: bool = False, model_name: str = "google/gemma-2b-it"):
        """Initialize single shared model instance"""
        self.model = GemmaModel(use_api=use_api, model_name=model_name)

    def get_model(self) -> GemmaModel:
        """Get model instance"""
        return self.model
