import pytest
import os
import logging
from utils.api_client import ApiClient

logger = logging.getLogger(__name__)

# Common issues in this file:
# 1. Hardcoded credentials (should use environment variables)
# 2. No validation of token format
# 3. No test for invalid credentials
# 4. No test for token expiration
# 5. No test for token refresh

# Test data
TEST_CREDENTIALS = {
    "username": os.getenv("API_USERNAME", "testuser"),
    "password": os.getenv("API_PASSWORD", "password")
}

INVALID_CREDENTIALS = {
    "username": "invalid_user",
    "password": "invalid_password"
}

@pytest.fixture(scope="module")
def api_client():
    """
    Module-scoped fixture for API client.
    """
    base_url = os.getenv("API_BASE_URL", "https://api.example.com")
    client = ApiClient(base_url)
    
    yield client
    
    # Cleanup
    client.close()


class TestAuthApi:
    """
    Tests for the Authentication API.
    """
    
    @pytest.mark.smoke
    def test_login_success(self, api_client):
        """
        Test successful login.
        """
        response = api_client.post("/auth/login", json=TEST_CREDENTIALS)
        
        # Verify response
        assert "token" in response, "Response should contain token"
        assert isinstance(response["token"], str), "Token should be a string"
        assert len(response["token"]) > 0, "Token should not be empty"
    
    @pytest.mark.api
    def test_login_invalid_credentials(self, api_client):
        """
        Test login with invalid credentials.
        """
        with pytest.raises(Exception) as excinfo:
            api_client.post("/auth/login", json=INVALID_CREDENTIALS)
        
        assert "401" in str(excinfo.value), "Should return 401 for invalid credentials"
    
    @pytest.mark.api
    def test_login_missing_credentials(self, api_client):
        """
        Test login with missing credentials.
        """
        with pytest.raises(Exception) as excinfo:
            api_client.post("/auth/login", json={"username": TEST_CREDENTIALS["username"]})
        
        assert "400" in str(excinfo.value), "Should return 400 for missing credentials"
    
    @pytest.mark.integration
    def test_access_protected_endpoint(self, api_client):
        """
        Test accessing a protected endpoint with a valid token.
        """
        # Login to get token
        login_response = api_client.post("/auth/login", json=TEST_CREDENTIALS)
        token = login_response.get("token")
        
        # Set token in client
        api_client.set_auth_token(token)
        
        # Access protected endpoint
        response = api_client.get("/users/me")
        
        # Verify response
        assert "id" in response, "Response should contain user ID"
        assert "username" in response, "Response should contain username"
        assert response.get("username") == TEST_CREDENTIALS["username"], "Username should match"
    
    @pytest.mark.integration
    def test_access_protected_endpoint_without_token(self, api_client):
        """
        Test accessing a protected endpoint without a token.
        """
        # Remove token from client
        api_client.session.headers.pop("Authorization", None)
        
        # Attempt to access protected endpoint
        with pytest.raises(Exception) as excinfo:
            api_client.get("/users/me")
        
        assert "401" in str(excinfo.value), "Should return 401 for missing token"
    
    @pytest.mark.api
    def test_logout(self, api_client):
        """
        Test logout functionality.
        """
        # Login to get token
        login_response = api_client.post("/auth/login", json=TEST_CREDENTIALS)
        token = login_response.get("token")
        
        # Set token in client
        api_client.set_auth_token(token)
        
        # Logout
        response = api_client.post("/auth/logout")
        
        # Verify response
        assert response.get("success") is True, "Logout should be successful"
        
        # Attempt to access protected endpoint after logout
        with pytest.raises(Exception) as excinfo:
            api_client.get("/users/me")
        
        assert "401" in str(excinfo.value), "Should return 401 after logout"