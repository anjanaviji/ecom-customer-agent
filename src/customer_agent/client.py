import requests
from .config import settings

class FakeApiClient:
    def __init__(self):
        self.base_url = settings.fake_api_base_url

    def get_user(self, user_id: int)->requests.Response:
        response = requests.get(f"{self.base_url}/users/{user_id}", timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    def get_order(self, order_id: int)->requests.Response:
            response = requests.get(f"{self.base_url}/orders/{order_id}", timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
    def get_user_orders(self, user_id: int)->requests.Response:
            response = requests.get(f"{self.base_url}/users/{user_id}/orders", timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()