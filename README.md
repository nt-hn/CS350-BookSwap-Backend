# Backend Endpoints Documentation

This document provides details about the backend endpoints available in our application. Each endpoint is listed with the required request type and necessary fields.

## Table of Contents
1. [Admin Panel Access](#admin-panel-access)
2. [Account API](#account-api)
   - [Register](#register)
   - [Token](#token)
   - [User](#user)

## Admin Panel Access

### Endpoint: `/admin/`
- **Description**: Access the admin panel.
- **Request Type**: Direct access through a web browser.
- **Authentication**: Admin login credentials are required (`email`,`password`).

## Account API

### Register

#### Endpoint: `/account_api/register/`
- **Description**: Register a new user.
- **Request Type**: POST
- **Required Fields**:
  - `first_name`: User's first name.
  - `last_name`: User's last name.
  - `email`: User's email address.
  - `password`: User's password.

#### Example Request:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "your_password"
}
```

### Token

#### Endpoint: `/account_api/token/`
- **Description**: Obtain an authentication token.
- **Request Type**: POST
- **Required Fields**:
  - `email`: User's email address.
  - `password`: User's password.

#### Example Request:
```json
{
  "email": "john.doe@example.com",
  "password": "your_password"
}
```

### User

#### Endpoint: `/account_api/user/`
- **Description**: Retrieve the user details from the token.
- **Request Type**: GET
- **Headers**: 
  - Include the Bearer Token in the header.
    - `Authorization: Bearer <token_value>`

#### Example Header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Notes
- Ensure the Bearer Token is included correctly in the headers for endpoints that require it.
- The admin panel is accessible directly via a web browser and does not involve API calls. Use your admin credentials to log in.