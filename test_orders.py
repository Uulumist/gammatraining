import json
import pytest
import requests
import allure
from allure_commons.types import AttachmentType

# Constants
url = "https://your-api-url.com"  # Replace with your actual URL
username = "your_username"  # Replace with your actual username
password = "your_password"  # Replace with your actual password

@pytest.fixture(scope="session")
def authenticate():
    login_url = f"{url}/login/student"
    body = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, json=body)
    if response.status_code == 200:
        token = response.text.strip()
        if token:
            print("✅ Successfully logged in. Bearer Token:", token)
            return token
        else:
            pytest.fail("❌ Authentication failed: No token found in response.")
    else:
        pytest.fail(f"❌ Failed to authenticate. Status: {response.status_code}, Response: {response.text}")

class Helper:
    def attach_response(self, response):
        response = json.dumps(response, indent=4)
        allure.attach(body=response, name="API Response", attachment_type=AttachmentType.JSON)

class Headers:
    def __init__(self, token):
        self.basic = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

class Endpoints:
    def __init__(self):
        self.create_order = f"{url}/orders"  # Replace with your actual endpoint

class Payloads:
    def __init__(self):
        self.create_order = {
            # Your order payload here
            "item": "Test Item",
            "quantity": 1
        }

class OrdersAPI(Helper):
    def __init__(self, token):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers(token)

    def create_order(self):
        response = requests.post(
            url=self.endpoints.create_order,
            headers=self.headers.basic,
            json=self.payloads.create_order
        )
        print("Request URL:", self.endpoints.create_order)
        print("Request Headers:", self.headers.basic)
        print("Request Body:", self.payloads.create_order)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)
        print("Payload:", self.payloads.create_order)
        assert response.status_code == 200, response.json()
        self.attach_response(response.json())
        return response.json()

class BaseTest:
    pass

class TestOrders(BaseTest):
    def test_create_order(self, authenticate):
        # Pass the token from the authenticate fixture to the OrdersAPI constructor
        orders_api = OrdersAPI(token=authenticate)
        order = orders_api.create_order()
        # Add your assertions here