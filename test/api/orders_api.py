import requests
import json
from .helper import Helper
from .headers import Headers
from .endpoints import Endpoints
from .payloads import Payloads

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