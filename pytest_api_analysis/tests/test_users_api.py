import pytest
import os
import logging
from utils.api_client import ApiClient
from utils.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)

# Common issues in this file:
# 1. Hardcoded test data (should use fixtures or parameterization)
# 2. Insufficient error handling
# 3. No validation of response schemas
# 4. No test for error cases
# 5. No cleanup after tests

# Setup test data
TEST_USER_ID = 1
TEST_USER_DATA = {
    "name": "Test User",
    "email": "test@example.com",
    "phone": "123-456-7890"
}

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

@pytest.fixture(scope="module")
def schema_validator():
    """
    Module-scoped fixture for schema validator.
    """
    return SchemaValidator(schema_dir="schemas")

@pytest.fixture
def create_test_user(api_client):
    """
    Fixture to create a test user and clean up after test.
    """
    # Create test user
    response = api_client.post("/users", json=TEST_USER_DATA)
    user_id = response.get("id")
    
    yield user_id
    
    # Clean up - delete test user
    try:
        api_client.delete(f"/users/{user_id}")
    except Exception as e:
        logger.warning(f"Failed to delete test user {user_id}: {str(e)}")


class TestUsersApi:
    """
    Tests for the Users API.
    """
    
    @pytest.mark.smoke
    def test_get_users(self, api_client, schema_validator):
        """
        Test getting a list of users.
        """
        response = api_client.get("/users")
        
        # Verify response
        assert isinstance(response, list), "Response should be a list"
        assert len(response) > 0, "Response should contain at least one user"
        
        # Validate schema
        for user in response:
            assert schema_validator.validate(user, "user"), "User schema validation failed"
    
    @pytest.mark.smoke
    def test_get_user_by_id(self, api_client, schema_validator):
        """
        Test getting a user by ID.
        """
        response = api_client.get(f"/users/{TEST_USER_ID}")
        
        # Verify response
        assert response.get("id") == TEST_USER_ID, f"User ID should be {TEST_USER_ID}"
        
        # Validate schema
        assert schema_validator.validate(response, "user"), "User schema validation failed"
    
    @pytest.mark.integration
    def test_create_user(self, api_client, schema_validator):
        """
        Test creating a new user.
        """
        # Create user
        response = api_client.post("/users", json=TEST_USER_DATA)
        
        # Verify response
        assert "id" in response, "Response should contain user ID"
        assert response.get("name") == TEST_USER_DATA["name"], "User name should match"
        assert response.get("email") == TEST_USER_DATA["email"], "User email should match"
        
        # Validate schema
        assert schema_validator.validate(response, "user"), "User schema validation failed"
        
        # Clean up - delete created user
        user_id = response.get("id")
        api_client.delete(f"/users/{user_id}")
    
    @pytest.mark.integration
    def test_update_user(self, api_client, create_test_user):
        """
        Test updating a user.
        """
        user_id = create_test_user
        
        # Update user
        updated_data = {
            "name": "Updated User",
            "email": "updated@example.com"
        }
        
        response = api_client.put(f"/users/{user_id}", json=updated_data)
        
        # Verify response
        assert response.get("id") == user_id, f"User ID should be {user_id}"
        assert response.get("name") == updated_data["name"], "User name should be updated"
        assert response.get("email") == updated_data["email"], "User email should be updated"
    
    @pytest.mark.integration
    def test_delete_user(self, api_client, create_test_user):
        """
        Test deleting a user.
        """
        user_id = create_test_user
        
        # Delete user
        response = api_client.delete(f"/users/{user_id}")
        
        # Verify response
        assert response.get("success") is True, "Deletion should be successful"
        
        # Verify user is deleted
        with pytest.raises(Exception) as excinfo:
            api_client.get(f"/users/{user_id}")
        
        assert "404" in str(excinfo.value), "User should not exist after deletion"
    
    @pytest.mark.api
    def test_get_nonexistent_user(self, api_client):
        """
        Test getting a non-existent user.
        """
        non_existent_id = 9999
        
        # Attempt to get non-existent user
        with pytest.raises(Exception) as excinfo:
            api_client.get(f"/users/{non_existent_id}")
        
        assert "404" in str(excinfo.value), "Should return 404 for non-existent user"
    
    @pytest.mark.api
    def test_create_user_invalid_data(self, api_client):
        """
        Test creating a user with invalid data.
        """
        invalid_data = {
            "name": "Invalid User",
            # Missing required email field
        }
        
        # Attempt to create user with invalid data
        with pytest.raises(Exception) as excinfo:
            api_client.post("/users", json=invalid_data)
        
        assert "400" in str(excinfo.value), "Should return 400 for invalid data"