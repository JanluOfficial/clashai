__version__ = "1.0.7"

import requests
import os

class Client:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key if api_key else os.getenv("CLASHAI_API_KEY")
        self.base_url = base_url if base_url else "https://api.clashai.eu"
        self.chat = Chat(self.api_key, self.base_url)
        self.images = Images(self.api_key, self.base_url)

    def models(self):
        # * Gets the models json located at api.clashai.eu/v1/models
        # ! Does not send API key as it's not required.
        endpoint = "v1/models"
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url) # , headers={"Authorization": f"Bearer {self.api_key}"}
        return response.json()

class Chat:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.completions = Completions(api_key, base_url)

class Completions:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key if api_key else os.getenv("CLASHAI_API_KEY")
        self.base_url = base_url if base_url else "https://api.clashai.eu"

    def create(self, messages: list, model: str = "chatgpt-4o-latest"):
        api_key = self.api_key
        endpoint = "v1/chat/completions"
        url = f"{self.base_url}/{endpoint}"
        payload = {
            "model": model,
            "messages": messages,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

class Images:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key if api_key else os.getenv("CLASHAI_API_KEY")
        self.base_url = base_url if base_url else "https://api.clashai.eu"

    def generate(self, prompt: str, model: str = "imagen-3.0-generate-001", n: int = 1, size: str = "256x256"):
        api_key = self.api_key
        endpoint = "v1/images/generations"
        url = f"{self.base_url}/{endpoint}"
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": response.status_code if 'response' in locals() else None}