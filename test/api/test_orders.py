import pytest
from .base_test import BaseTest
from .orders_api import OrdersAPI

class TestOrders(BaseTest):
    def test_create_order(self, authenticate):
        # Pass the token from the authenticate fixture to the OrdersAPI constructor
        orders_api = OrdersAPI(token=authenticate)
        order = orders_api.create_order()
        # Add any assertions on the order response here