"""Auto-documentation decorators for Swagger/OpenAPI"""

from typing import Dict, Any, Optional


def document_endpoint(
    summary: str,
    description: str = "",
    tags: list = None,
    responses: Dict[int, str] = None,
    parameters: list = None,
    request_body: Dict[str, Any] = None,
    security: list = None
):
    """
    Decorator to auto-document API endpoints.
    
    Args:
        summary: Short summary of endpoint
        description: Detailed description
        tags: List of tags for grouping
        responses: Dictionary of status codes and descriptions
        parameters: List of query/path parameters
        request_body: Request body schema
        security: Security requirements (e.g., ['BearerAuth'])
    """
    def decorator(func):
        func.__swagger_spec__ = {
            'summary': summary,
            'description': description,
            'tags': tags or [],
            'responses': responses or {},
            'parameters': parameters or [],
            'requestBody': request_body,
            'security': security or []
        }
        return func
    return decorator


def build_spec_from_decorators(routes_info: list) -> Dict[str, Any]:
    """
    Build OpenAPI spec from decorated endpoints.
    
    Args:
        routes_info: List of (path, method, function) tuples
        
    Returns:
        OpenAPI paths specification
    """
    paths = {}
    
    for path, method, func in routes_info:
        if not hasattr(func, '__swagger_spec__'):
            continue
            
        spec = func.__swagger_spec__
        method_lower = method.lower()
        
        if path not in paths:
            paths[path] = {}
        
        paths[path][method_lower] = {
            'tags': spec['tags'],
            'summary': spec['summary'],
            'description': spec['description'],
            'parameters': spec['parameters'],
            'requestBody': spec['requestBody'],
            'responses': spec['responses'],
            'security': spec['security']
        }
        
        # Remove None values
        paths[path][method_lower] = {
            k: v for k, v in paths[path][method_lower].items() 
            if v is not None
        }
    
    return paths
