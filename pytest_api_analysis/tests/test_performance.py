import pytest
import time
import logging
import os
from utils.api_client import ApiClient

logger = logging.getLogger(__name__)

# Common issues in this file:
# 1. Hardcoded performance thresholds (should be configurable)
# 2. No consideration for network latency
# 3. No parallel testing
# 4. No load testing
# 5. No reporting of performance metrics

# Performance thresholds
RESPONSE_TIME_THRESHOLD = float(os.getenv("RESPONSE_TIME_THRESHOLD", "1.0"))  # seconds
CONCURRENT_USERS = int(os.getenv("CONCURRENT_USERS", "5"))

@pytest.fixture(scope="module")
def api_client():
    """
    Module-scoped fixture for API client.
    """
    base_url = os.getenv("API_BASE_URL", "https://api.example.com")
    client = ApiClient(base_url)
    
    # Get authentication token
    auth_response = client.post("/auth/login", json={
        "username": os.getenv("API_USERNAME", "testuser"),
        "password": os.getenv("API_PASSWORD", "password")
    })
    
    token = auth_response.get("token")
    if not token:
        pytest.fail("Failed to get authentication token")
    
    client.set_auth_token(token)
    
    yield client
    
    # Cleanup
    client.close()


class TestApiPerformance:
    """
    Performance tests for the API.
    """
    
    @pytest.mark.performance
    def test_users_endpoint_response_time(self, api_client):
        """
        Test response time for the users endpoint.
        """
        start_time = time.time()
        api_client.get("/users")
        end_time = time.time()
        
        response_time = end_time - start_time
        logger.info(f"Response time for /users: {response_time:.4f} seconds")
        
        assert response_time < RESPONSE_TIME_THRESHOLD, f"Response time should be less than {RESPONSE_TIME_THRESHOLD} seconds"
    
    @pytest.mark.performance
    def test_user_endpoint_response_time(self, api_client):
        """
        Test response time for the user endpoint.
        """
        user_id = 1
        
        start_time = time.time()
        api_client.get(f"/users/{user_id}")
        end_time = time.time()
        
        response_time = end_time - start_time
        logger.info(f"Response time for /users/{user_id}: {response_time:.4f} seconds")
        
        assert response_time < RESPONSE_TIME_THRESHOLD, f"Response time should be less than {RESPONSE_TIME_THRESHOLD} seconds"
    
    @pytest.mark.performance
    def test_sequential_requests(self, api_client):
        """
        Test response time for sequential requests.
        """
        endpoints = ["/users", "/products", "/orders"]
        total_time = 0
        
        for endpoint in endpoints:
            start_time = time.time()
            api_client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            logger.info(f"Response time for {endpoint}: {response_time:.4f} seconds")
            
            total_time += response_time
            
            assert response_time < RESPONSE_TIME_THRESHOLD, f"Response time for {endpoint} should be less than {RESPONSE_TIME_THRESHOLD} seconds"
        
        logger.info(f"Total time for sequential requests: {total_time:.4f} seconds")
    
    @pytest.mark.performance
    @pytest.mark.parametrize("user_id", range(1, 6))
    def test_parametrized_requests(self, api_client, user_id):
        """
        Test response time for parametrized requests.
        """
        start_time = time.time()
        api_client.get(f"/users/{user_id}")
        end_time = time.time()
        
        response_time = end_time - start_time
        logger.info(f"Response time for /users/{user_id}: {response_time:.4f} seconds")
        
        assert response_time < RESPONSE_TIME_THRESHOLD, f"Response time for /users/{user_id} should be less than {RESPONSE_TIME_THRESHOLD} seconds"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_repeated_requests(self, api_client):
        """
        Test response time for repeated requests.
        """
        endpoint = "/users"
        num_requests = 10
        response_times = []
        
        for i in range(num_requests):
            start_time = time.time()
            api_client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        logger.info(f"Average response time for {endpoint}: {avg_response_time:.4f} seconds")
        logger.info(f"Maximum response time for {endpoint}: {max_response_time:.4f} seconds")
        logger.info(f"Minimum response time for {endpoint}: {min_response_time:.4f} seconds")
        
        assert avg_response_time < RESPONSE_TIME_THRESHOLD, f"Average response time should be less than {RESPONSE_TIME_THRESHOLD} seconds"
        assert max_response_time < RESPONSE_TIME_THRESHOLD * 2, f"Maximum response time should be less than {RESPONSE_TIME_THRESHOLD * 2} seconds"