from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample user data (in a real app, this would be a database)
users = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "developer"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "designer"},
    {"id": 3, "name": "Charlie Davis", "email": "charlie@example.com", "role": "manager"},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com", "role": "developer"}
]

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Resource not found",
        "message": "The requested URL was not found on the server"
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred on the server"
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all uncaught exceptions"""
    # Log the error (in production, you'd use proper logging)
    print(f"Unhandled exception: {str(error)}")
    
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    """Return all users"""
    try:
        return jsonify({"users": users}), 200
    except Exception as e:
        raise Exception(f"Error fetching users: {str(e)}")

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a specific user by ID"""
    try:
        user = next((u for u in users if u["id"] == user_id), None)
        
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user), 200
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Check if JSON data was provided
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate required fields
        if not all(key in data for key in ['name', 'email', 'role']):
            return jsonify({"error": "Missing required fields: name, email, role"}), 400
        
        # Validate email format (basic check)
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Create new user with auto-incrementing ID
        new_user = {
            "id": max(u["id"] for u in users) + 1 if users else 1,
            "name": data["name"],
            "email": data["email"],
            "role": data["role"]
        }
        
        users.append(new_user)
        return jsonify(new_user), 201
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")

# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        user = next((u for u in users if u["id"] == user_id), None)
        
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Check if JSON data was provided
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Update user fields
        if 'name' in data:
            user['name'] = data['name']
        if 'email' in data:
            if '@' not in data['email']:
                return jsonify({"error": "Invalid email format"}), 400
            user['email'] = data['email']
        if 'role' in data:
            user['role'] = data['role']
        
        return jsonify(user), 200
    except Exception as e:
        raise Exception(f"Error updating user: {str(e)}")

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        user = next((u for u in users if u["id"] == user_id), None)
        
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        users.remove(user)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        raise Exception(f"Error deleting user: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)