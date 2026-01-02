# REST API Testing with Postman

A demonstration of API testing using Postman with a Flask REST API for user management.

## Overview

This project includes:
- A Flask REST API with full CRUD operations for user management
- Postman collection with automated test assertions
- Error handling for common HTTP status codes (400, 404, 500)

## Technologies Used

- **Flask** - Python web framework for building the REST API
- **Postman** - API testing and documentation
- **Python 3.12**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/users/<id>` | Get a specific user by ID |
| POST | `/users` | Create a new user |
| PUT | `/users/<id>` | Update an existing user |
| DELETE | `/users/<id>` | Delete a user |

## Setup Instructions

### Prerequisites
- Python 3.12+
- Postman (download from https://www.postman.com/downloads/)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/joemarino-dev/rest-api-testing.git
cd rest-api-testing
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask API:
```bash
python user_api.py
```

The API will be running at `http://127.0.0.1:5001`

### Import Postman Collection

1. Open Postman
2. Click **Import** button
3. Select `User_API_Tests.postman_collection.json`
4. The collection will appear in your Collections sidebar

## Running Tests

1. Make sure the Flask API is running (`python user_api.py`)
2. In Postman, open the "User API Tests" collection
3. Click **Run** button to execute all tests
4. View test results to see pass/fail status

## Test Coverage

The Postman collection includes automated tests for:
- Response status codes (200, 201, 400, 404, 500)
- JSON response structure validation
- Data type validation
- Error message validation
- CRUD operation verification

## Sample Requests

### Create a User
```json
POST /users
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "developer"
}
```

### Update a User
```json
PUT /users/1
{
  "role": "senior developer"
}
```

## Error Handling

The API handles the following error scenarios:
- **400 Bad Request** - Missing required fields or invalid data
- **404 Not Found** - User or endpoint doesn't exist
- **500 Internal Server Error** - Unexpected server errors

## Author

Joe Marino - QA Engineer / SDET
- GitHub: [@joemarino-dev](https://github.com/joemarino-dev)

## Future Enhancements

- [ ] Add authentication/authorization
- [ ] Connect to a real database (PostgreSQL/MongoDB)
- [ ] Add pagination for user list
- [ ] Add search/filter functionality
- [ ] Implement rate limiting