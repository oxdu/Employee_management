Testing Authentication APIs
A. Register New User
Request:

Method: POST
URL: http://localhost:8000/api/auth/register/
Headers:

Content-Type: application/json


Body (raw JSON):

json{
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}
Expected Response:
json{
    "refresh": "ey.......",
    "access": "ey......",
    "user": {
        "id": 1,
        "email": "testuser@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "phone": null
    }
}

B. Login
Request:

Method: POST
URL: http://localhost:8000/api/auth/login/
Headers:

Content-Type: application/json


Body (raw JSON):

json{
    "email": "testuser@example.com",
    "password": "testpass123"
}

C. Setting Up Authorization in Postman
After login, you need to use the access token for all protected endpoints:

Copy the access token from the login response
In Postman, go to the "Authorization" tab
Select Type: "Bearer Token"
Paste your access token in the Token field
