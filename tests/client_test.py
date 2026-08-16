from customer_agent.client import FakeApiClient

def test_get_user_success(requests_mock):
    client = FakeApiClient()
    user_id = 1

    requests_mock.get(
        f"https://fakeapi.net/users/{user_id}",
        json={
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
        },
    )
    user = client.get_user(user_id)
    assert user["id"] == 1
    assert user["name"] == "John Doe"
    assert user["email"] == "john@example.com"

def test_get_user_orders_success(requests_mock):
    client = FakeApiClient()

    requests_mock.get(
        "https://fakeapi.net/users/1/orders",
        status_code=200,
        json=[{"id":1,"userId":1,"products":[{"productId":1,"quantity":2},{"productId":2,"quantity":1}],
               "totalAmount":1629.97,"status":"delivered","orderDate":"2024-01-15","deliveryDate":"2024-01-20"},
               {"id":2,"userId":1,"products":[{"productId":3,"quantity":1}],"totalAmount":149.99,"status":"processing",
                "orderDate":"2024-02-01","deliveryDate":None}]
    )

    response = client.get_user_orders(1)

    assert response[0]["id"] == 1
