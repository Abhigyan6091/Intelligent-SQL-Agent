# llm_clients.py
import os
from openai import OpenAI
from mistralai import Mistral
import json



class OpenAIClient:
    def __init__(self, model="gpt-4o-mini", api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def complete(self, prompt: str, max_tokens=300):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert SQL generator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0,
        )
        return response.choices[0].message.content.strip()


class MistralClient:
    def __init__(self, model="mistral-small-latest", api_key=None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.model = model
        self.client = Mistral(api_key=self.api_key)

    def complete(self, prompt: str, max_tokens=300):
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert SQL generator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0,
        )
        return response.choices[0].message["content"].strip()
