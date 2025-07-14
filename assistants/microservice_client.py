import requests
from django.conf import settings

class MicroserviceClient:
    def __init__(self):
        self.base_url = settings.MICROSERVICE_URL
        self.api_key = settings.MICROSERVICE_API_KEY
        self.headers = {"X-API-Key": self.api_key}

    def create_assistant(self, name, instructions, model):
        url = f"{self.base_url}/api/assistants"
        payload = {
            "name": name,
            "instructions": instructions,
            "model": model,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def upload_file(self, file):
        url = f"{self.base_url}/api/files"
        files = {"upload": (file.name, file.read(), file.content_type)}
        response = requests.post(url, headers=self.headers, files=files)
        response.raise_for_status()
        return response.json()

    def create_vector_store(self, name):
        url = f"{self.base_url}/api/vector_stores"
        payload = {"name": name}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def add_file_to_vector_store(self, store_id, file_id):
        url = f"{self.base_url}/api/vector_stores/{store_id}/files"
        payload = [file_id]
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def update_assistant_vector_store(self, assistant_id, vector_store_id):
        url = f"{self.base_url}/api/assistants/{assistant_id}"
        payload = {"vector_store_id": vector_store_id}
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_thread(self, initial_message):
        url = f"{self.base_url}/api/create_thread"
        payload = {"initial_message": initial_message}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def run_thread(self, thread_id, assistant_id):
        url = f"{self.base_url}/api/run"
        payload = {"thread_id": thread_id, "assistant_id": assistant_id}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_thread_status(self, thread_id):
        url = f"{self.base_url}/api/thread_status/{thread_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_latest_message(self, thread_id):
        url = f"{self.base_url}/api/latest_message/{thread_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
