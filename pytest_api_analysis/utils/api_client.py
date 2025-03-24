import os
import json
import logging
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger(__name__)

class ApiClient:
    """
    API Client for making HTTP requests with error handling and logging.
    """
    
    def __init__(self, base_url, timeout=10, headers=None):
        """
        Initialize the API client.
        
        Args:
            base_url (str): Base URL for the API
            timeout (int): Request timeout in seconds
            headers (dict): Default headers for requests
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if headers:
            default_headers.update(headers)
            
        self.session.headers.update(default_headers)
    
    def set_auth_token(self, token):
        """
        Set authentication token in headers.
        
        Args:
            token (str): Authentication token
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def _build_url(self, endpoint):
        """
        Build full URL from endpoint.
        
        Args:
            endpoint (str): API endpoint
            
        Returns:
            str: Full URL
        """
        # Remove leading slash from endpoint if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
            
        return f"{self.base_url}/{endpoint}"
    
    def _handle_response(self, response):
        """
        Handle API response, log details, and raise exceptions for errors.
        
        Args:
            response (Response): Response object from requests
            
        Returns:
            dict: Response data
            
        Raises:
            Exception: If response status code indicates an error
        """
        logger.debug(f"Response status: {response.status_code}")
        
        try:
            response_data = response.json() if response.text else {}
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response.text}")
            response_data = {"error": "Invalid JSON response", "text": response.text}
        
        # Log response details for debugging
        if response.status_code >= 400:
            logger.error(f"API error: {response.status_code} - {response_data}")
            response.raise_for_status()
            
        return response_data
    
    def request(self, method, endpoint, **kwargs):
        """
        Make an HTTP request with error handling.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint (str): API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data
            
        Raises:
            RequestException: If request fails
        """
        url = self._build_url(endpoint)
        timeout = kwargs.pop('timeout', self.timeout)
        
        # Log request details
        logger.info(f"{method} {url}")
        if 'json' in kwargs:
            logger.debug(f"Request data: {kwargs['json']}")
        
        try:
            response = self.session.request(method, url, timeout=timeout, **kwargs)
            return self._handle_response(response)
        except Timeout:
            logger.error(f"Request timeout: {method} {url}")
            raise
        except ConnectionError:
            logger.error(f"Connection error: {method} {url}")
            raise
        except RequestException as e:
            logger.error(f"Request failed: {method} {url} - {str(e)}")
            raise
    
    def get(self, endpoint, params=None, **kwargs):
        """
        Make a GET request.
        
        Args:
            endpoint (str): API endpoint
            params (dict): Query parameters
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data
        """
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint, data=None, json=None, **kwargs):
        """
        Make a POST request.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Form data
            json (dict): JSON data
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data
        """
        return self.request('POST', endpoint, data=data, json=json, **kwargs)
    
    def put(self, endpoint, data=None, json=None, **kwargs):
        """
        Make a PUT request.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Form data
            json (dict): JSON data
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data
        """
        return self.request('PUT', endpoint, data=data, json=json, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """
        Make a DELETE request.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data
        """
        return self.request('DELETE', endpoint, **kwargs)
    
    def close(self):
        """
        Close the session.
        """
        self.session.close()