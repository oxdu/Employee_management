# Authentication API Documentation

This document provides comprehensive testing instructions for the Authentication API endpoints.

## Base URL
```
http://localhost:8000/api/auth/
```

## API Endpoints

### A. Register New User

**Endpoint:** `POST /api/auth/register/`

**Description:** Register a new user account and receive authentication tokens.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}
```

**Expected Response:**
```json
{
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
```

**Status Codes:**
- `201 Created` - User successfully registered
- `400 Bad Request` - Invalid data or user already exists

---

### B. Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate existing user and receive access tokens.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "testuser@example.com",
    "password": "testpass123"
}
```

**Expected Response:**
```json
{
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
```

**Status Codes:**
- `200 OK` - Login successful
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing required fields

---

## Testing with Postman

### Setting Up Authorization

After successful login or registration, you'll receive an access token. To use protected endpoints:

1. **Copy the access token** from the login/register response
2. **In Postman:**
   - Go to the **Authorization** tab
   - Select **Type: Bearer Token**
   - Paste your access token in the **Token** field
3. **For collection-level auth:**
   - Right-click your collection → Edit
   - Go to Authorization tab
   - Set Bearer Token there to apply to all requests

## Then Try with all endpoints
