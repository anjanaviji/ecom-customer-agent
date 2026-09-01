from .client import FakeApiClient
from langchain.tools import tool

@tool
def get_order(order_id: int)->dict:
    """Get order details by order ID using the provided"""
    client = FakeApiClient()
    return client.get_order(order_id)
@tool
def get_user(user_id: int)->dict:
    """Get user details by user ID using the provided"""
    client = FakeApiClient()
    return client.get_user(user_id)
@tool
def get_user_orders(user_id: int)->list:
    """Get all orders for a specific user"""
    client = FakeApiClient()
    return client.get_user_orders(user_id)