import json
import logging
import os
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class SchemaValidator:
    """
    Utility class for validating API responses against JSON schemas.
    """
    
    def __init__(self, schema_dir="schemas"):
        """
        Initialize the schema validator.
        
        Args:
            schema_dir (str): Directory containing schema files
        """
        self.schema_dir = schema_dir
        self.schemas = {}
        
        # Load schemas if directory exists
        if os.path.exists(schema_dir):
            self._load_schemas()
    
    def _load_schemas(self):
        """
        Load all schema files from the schema directory.
        """
        for filename in os.listdir(self.schema_dir):
            if filename.endswith('.json'):
                schema_name = os.path.splitext(filename)[0]
                schema_path = os.path.join(self.schema_dir, filename)
                
                try:
                    with open(schema_path, 'r') as f:
                        self.schemas[schema_name] = json.load(f)
                    logger.debug(f"Loaded schema: {schema_name}")
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f"Failed to load schema {schema_name}: {str(e)}")
    
    def get_schema(self, schema_name):
        """
        Get a schema by name.
        
        Args:
            schema_name (str): Name of the schema
            
        Returns:
            dict: Schema definition
            
        Raises:
            ValueError: If schema not found
        """
        if schema_name not in self.schemas:
            schema_path = os.path.join(self.schema_dir, f"{schema_name}.json")
            
            if not os.path.exists(schema_path):
                raise ValueError(f"Schema not found: {schema_name}")
            
            try:
                with open(schema_path, 'r') as f:
                    self.schemas[schema_name] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Failed to load schema {schema_name}: {str(e)}")
                raise ValueError(f"Failed to load schema {schema_name}: {str(e)}")
        
        return self.schemas[schema_name]
    
    def validate(self, data, schema_name):
        """
        Validate data against a schema.
        
        Args:
            data (dict): Data to validate
            schema_name (str): Name of the schema
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValueError: If schema not found
        """
        schema = self.get_schema(schema_name)
        
        try:
            validate(instance=data, schema=schema)
            logger.debug(f"Validation passed for schema: {schema_name}")
            return True
        except ValidationError as e:
            logger.error(f"Validation failed for schema {schema_name}: {str(e)}")
            return False
    
    def validate_or_fail(self, data, schema_name):
        """
        Validate data against a schema and raise an exception if invalid.
        
        Args:
            data (dict): Data to validate
            schema_name (str): Name of the schema
            
        Raises:
            ValidationError: If validation fails
            ValueError: If schema not found
        """
        schema = self.get_schema(schema_name)
        validate(instance=data, schema=schema)
        logger.debug(f"Validation passed for schema: {schema_name}")
        return True