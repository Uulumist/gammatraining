import os
import pytest
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration constants
BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("API_KEY", "")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Common issues:
# 1. Hardcoded credentials or URLs (should use environment variables)
# 2. No environment-specific configuration
# 3. Missing error handling for environment variables


@pytest.fixture(scope="session")
def api_client():
    """
    Session-scoped fixture for API client.
    Provides a configured session for making API requests.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })
    
    # Add request timeout to avoid hanging tests
    session.request = lambda method, url, **kwargs: requests.Session.request(
        session, method, url, timeout=TIMEOUT, **kwargs
    )
    
    yield session
    
    # Clean up session after tests
    session.close()


@pytest.fixture(scope="function")
def auth_token():
    """
    Function-scoped fixture for authentication token.
    Gets a new token for each test that requires authentication.
    """
    # Example token retrieval logic
    response = requests.post(
        f"{BASE_URL}/auth/token",
        json={"username": os.getenv("API_USERNAME"), "password": os.getenv("API_PASSWORD")},
        timeout=TIMEOUT
    )
    
    if response.status_code != 200:
        pytest.fail(f"Failed to get auth token: {response.text}")
    
    token = response.json().get("token")
    return token


@pytest.fixture
def test_data():
    """
    Fixture providing test data.
    """
    return {
        "user": {
            "name": "Test User",
            "email": "test@example.com"
        },
        "product": {
            "name": "Test Product",
            "price": 99.99
        }
    }


# Reporting and logging setup
def pytest_configure(config):
    """
    Configure pytest with custom settings.
    """
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "api: mark test as API test")


# Hooks for test result handling
def pytest_runtest_setup(item):
    """
    Called before each test is run.
    """
    # Example: Log test start
    print(f"\nStarting test: {item.name}")


def pytest_runtest_teardown(item):
    """
    Called after each test is run.
    """
    # Example: Log test end
    print(f"Finished test: {item.name}")