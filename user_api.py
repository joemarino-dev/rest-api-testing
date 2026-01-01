"""
REST API for User Management
=============================
A Flask-based RESTful API that provides CRUD (Create, Read, Update, Delete) 
operations for managing user data.

This API demonstrates:
- RESTful endpoint design
- HTTP method handling (GET, POST, PUT, DELETE)
- JSON request/response formatting
- Input validation and error handling
- Proper HTTP status codes (200, 201, 400, 404, 500)

Author: Joe Marino
GitHub: https://github.com/joemarino-dev/rest-api-testing
"""

from flask import Flask, request, jsonify

# Initialize Flask application
# __name__ helps Flask determine the root path for the application
app = Flask(__name__)

# ============================================================================
# DATA STORAGE
# ============================================================================
# In-memory user data storage (list of dictionaries)
# NOTE: In a production environment, this would be replaced with a database
# (e.g., PostgreSQL, MySQL, MongoDB). Changes to this list are not persistent
# and will be lost when the server restarts.
users = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "developer"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "designer"},
    {"id": 3, "name": "Charlie Davis", "email": "charlie@example.com", "role": "manager"},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com", "role": "developer"}
]

# ============================================================================
# ERROR HANDLERS
# ============================================================================
# These decorators catch specific HTTP errors and return consistent JSON responses
# instead of Flask's default HTML error pages

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 Not Found errors
    
    Triggered when:
    - A requested endpoint doesn't exist (e.g., /invalid-endpoint)
    - A route is accessed with the wrong HTTP method
    
    Args:
        error: The error object from Flask (not used but required by decorator)
        
    Returns:
        tuple: (JSON error response, 404 HTTP status code)
    """
    return jsonify({
        "error": "Resource not found",
        "message": "The requested URL was not found on the server"
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle 500 Internal Server Error
    
    Triggered when:
    - An unhandled exception occurs in the application
    - Database connection fails (if using a database)
    - Any unexpected server-side error
    
    Args:
        error: The error object from Flask
        
    Returns:
        tuple: (JSON error response, 500 HTTP status code)
    """
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred on the server"
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """
    Catch-all handler for any uncaught exceptions
    
    This acts as a safety net to prevent the server from crashing and
    ensures all errors return a consistent JSON format instead of exposing
    stack traces to the client.
    
    Args:
        error: The exception object that was raised
        
    Returns:
        tuple: (JSON error response, 500 HTTP status code)
        
    Note:
        In production, replace print() with proper logging (e.g., Python's
        logging module or a service like Sentry)
    """
    # Log the error for debugging
    # TODO: Replace with proper logging framework in production
    print(f"Unhandled exception: {str(error)}")
    
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

# ============================================================================
# API ENDPOINTS - USER OPERATIONS
# ============================================================================

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve all users from the system
    
    Endpoint: GET /users
    
    Returns:
        tuple: (JSON response with array of users, 200 status code)
        
    Example Response:
        {
            "users": [
                {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "developer"},
                ...
            ]
        }
        
    Error Handling:
        - Catches any exceptions and re-raises them to be handled by global error handler
    """
    try:
        # Return the entire users list wrapped in a "users" key
        return jsonify({"users": users}), 200
    except Exception as e:
        # Re-raise with more context for debugging
        raise Exception(f"Error fetching users: {str(e)}")

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a specific user by their ID
    
    Endpoint: GET /users/<user_id>
    
    Args:
        user_id (int): The unique identifier for the user (extracted from URL)
        
    Returns:
        tuple: (JSON response with user object, 200 status code) if found
        tuple: (JSON error response, 404 status code) if not found
        
    Example Request:
        GET /users/1
        
    Example Response (Success):
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "role": "developer"
        }
        
    Example Response (Not Found):
        {
            "error": "User not found"
        }
        
    Implementation Notes:
        - Uses next() with a generator expression to search the users list
        - Returns None if no user matches the ID
        - The <int:user_id> in the route ensures user_id is converted to integer
    """
    try:
        # Search for user with matching ID
        # next() returns the first match or None if no match found
        user = next((u for u in users if u["id"] == user_id), None)
        
        # Check if user was found
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        # Return the user object
        return jsonify(user), 200
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user in the system
    
    Endpoint: POST /users
    
    Request Body (JSON):
        {
            "name": "John Doe",          # Required
            "email": "john@example.com",  # Required, must contain @
            "role": "developer"           # Required
        }
        
    Returns:
        tuple: (JSON response with created user, 201 status code) on success
        tuple: (JSON error response, 400 status code) on validation failure
        
    Example Response (Success):
        {
            "id": 5,
            "name": "John Doe",
            "email": "john@example.com",
            "role": "developer"
        }
        
    Validation Rules:
        - All three fields (name, email, role) are required
        - Email must contain an @ symbol (basic validation)
        - Request must include valid JSON
        
    Implementation Notes:
        - Auto-generates ID by finding max existing ID and adding 1
        - If users list is empty, starts with ID 1
        - User is appended to the in-memory users list
        - Returns 201 (Created) status code on success per REST conventions
    """
    try:
        # Parse JSON from request body
        data = request.get_json()
        
        # Validate that JSON was provided
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate that all required fields are present
        # all() returns True only if ALL required keys exist in data
        if not all(key in data for key in ['name', 'email', 'role']):
            return jsonify({"error": "Missing required fields: name, email, role"}), 400
        
        # Basic email validation (just checks for @ symbol)
        # TODO: Consider using regex for more robust email validation
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Create new user dictionary with auto-generated ID
        # ID generation: find highest current ID and add 1, or use 1 if list is empty
        new_user = {
            "id": max(u["id"] for u in users) + 1 if users else 1,
            "name": data["name"],
            "email": data["email"],
            "role": data["role"]
        }
        
        # Add new user to the list
        users.append(new_user)
        
        # Return created user with 201 status code
        # 201 = Created (standard REST response for successful POST)
        return jsonify(new_user), 201
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user's information
    
    Endpoint: PUT /users/<user_id>
    
    Args:
        user_id (int): The ID of the user to update
        
    Request Body (JSON):
        Any combination of these fields:
        {
            "name": "Updated Name",      # Optional
            "email": "new@example.com",  # Optional, must contain @ if provided
            "role": "senior developer"   # Optional
        }
        
    Returns:
        tuple: (JSON response with updated user, 200 status code) on success
        tuple: (JSON error response, 404 status code) if user not found
        tuple: (JSON error response, 400 status code) on validation failure
        
    Example Request:
        PUT /users/1
        {
            "role": "senior developer"
        }
        
    Example Response (Success):
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "role": "senior developer"
        }
        
    Implementation Notes:
        - Partial updates allowed (only provide fields you want to change)
        - Validates email format if email is being updated
        - User object is modified in-place in the users list
        - Returns the full updated user object
    """
    try:
        # Find the user to update
        user = next((u for u in users if u["id"] == user_id), None)
        
        # Check if user exists
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        # Parse JSON from request body
        data = request.get_json()
        
        # Validate that JSON was provided
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Update fields that are present in the request
        # Only updates fields that are actually provided (partial update)
        if 'name' in data:
            user['name'] = data['name']
        if 'email' in data:
            # Validate email format if email is being updated
            if '@' not in data['email']:
                return jsonify({"error": "Invalid email format"}), 400
            user['email'] = data['email']
        if 'role' in data:
            user['role'] = data['role']
        
        # Return the updated user object
        # Note: The user object in the list is modified directly,
        # so we return the same reference
        return jsonify(user), 200
    except Exception as e:
        raise Exception(f"Error updating user: {str(e)}")

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user from the system
    
    Endpoint: DELETE /users/<user_id>
    
    Args:
        user_id (int): The ID of the user to delete
        
    Returns:
        tuple: (JSON success message, 200 status code) if user deleted
        tuple: (JSON error response, 404 status code) if user not found
        
    Example Request:
        DELETE /users/1
        
    Example Response (Success):
        {
            "message": "User deleted successfully"
        }
        
    Example Response (Not Found):
        {
            "error": "User not found"
        }
        
    Implementation Notes:
        - Removes the user from the in-memory users list
        - Once deleted, the user ID is not reused
        - In production with a database, consider soft deletes (marking as deleted)
          instead of hard deletes for audit trail purposes
    """
    try:
        # Find the user to delete
        user = next((u for u in users if u["id"] == user_id), None)
        
        # Check if user exists
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        # Remove user from the list
        # This modifies the users list in-place
        users.remove(user)
        
        # Return success message
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        raise Exception(f"Error deleting user: {str(e)}")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    """
    Start the Flask development server
    
    Configuration:
        - debug=True: Enables debug mode with auto-reload and detailed error pages
                     WARNING: Never use debug=True in production!
        - port=5001: Runs server on port 5001 to avoid conflicts with macOS AirPlay
                    which uses port 5000 by default
                    
    Access the API at: http://127.0.0.1:5001
    
    To stop the server: Press CTRL+C in the terminal
    
    Production Deployment Notes:
        - Use a production WSGI server (e.g., Gunicorn, uWSGI)
        - Set debug=False
        - Use environment variables for configuration
        - Implement authentication/authorization
        - Add rate limiting
        - Use a proper database instead of in-memory storage
    """
    app.run(debug=True, port=5001)