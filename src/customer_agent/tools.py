from .client import FakeApiClient
from langchain.tools import tool

@tool
def get_order(order_id: int)->dict:
    """Get order details by order ID using the provided"""
    client = FakeApiClient()
    return client.get_order(order_id)