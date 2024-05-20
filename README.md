# Backend Endpoints Documentation

This document provides details about the backend endpoints available in our application. Each endpoint is listed with the required request type and necessary fields.

## Table of Contents
1. [Admin Panel Access](#admin-panel-access)
2. [Account API](#account-api)
   - [Register](#register)
   - [Token](#token)
   - [User](#user)
3. [Book API](#book-api)
   - [List and Create Books](#list-and-create-books)
   - [Retrieve, Update, and Delete a Book](#retrieve-update-and-delete-a-book)

## Admin Panel Access

### Endpoint: `/admin/`
- **Description**: Access the admin panel.
- **Request Type**: Direct access through a web browser.
- **Authentication**: Admin login credentials are required (`email`, `password`).

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

---

# Book API

### List and Create Books

End point: `/book/`

#### Methods
- `GET`: Retrieve a list of all books. 
- `POST`: Create a new book. 

#### Request (GET)
No parameters are required.

#### Request (POST)
- **Authentication required**: Yes
- **Request body**:
    - `title`: String
    - `author`: String
    - `isbn`: String
    - `publication_date`: String (optional, format: 'YYYY-MM-DD')
    - `publisher`: String (optional)
    - `image`: File (optional)
    - `current_owner`: Will by default be set as the authenticated user.

#### Responses
- `200 OK`: A list of all books (for `GET`).
- `201 Created`: The created book object (for `POST`).
- `400 Bad Request`: Validation errors.
- `403 Forbidden`: Authentication credentials not provided or insufficient permissions.

#### Example

**GET Request**
```http
GET /books/ HTTP/1.1
Content-Type: application/json
```

**POST Request**
```http
POST /books/ HTTP/1.1
Content-Type: multipart/form-data
Authorization: Bearer <your_token>

{
    "title": "Book Title",
    "author": "Author Name",
    "isbn": "1234567890123",
    "publication_date": "2022-01-01",
    "publisher": "Publisher Name",
    "image": <file>,
}
```

### Retrieve, Update, and Delete a Book

End point: `/books/<id>/`

#### Methods
- `GET`: Retrieve a specific book by its ID.
- `PUT`: Update a specific book by its ID.
- `DELETE`: Delete a specific book by its ID.

#### Request (GET)
No parameters are required.

#### Request (PUT)
- **Authentication required**: Yes
- **Request body**:
    - `title`: String (optional)
    - `author`: String (optional)
    - `isbn`: String (optional)
    - `publication_date`: String (optional, format: 'YYYY-MM-DD')
    - `publisher`: String (optional)
    - `image`: File (optional)
    - `current_owner`: Will by default be the user currently authenticated

#### Request (DELETE)
- **Authentication required**: Yes

#### Responses
- `200 OK`: The requested book object (for `GET`).
- `200 OK`: The updated book object (for `PUT`).
- `204 No Content`: The book was successfully deleted (for `DELETE`).
- `400 Bad Request`: Validation errors.
- `403 Forbidden`: Authentication credentials not provided, insufficient permissions, or user is not the owner.
- `404 Not Found`: The book with the specified ID does not exist.

#### Example

**GET Request**
```http
GET /books/1/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <your_token>
```

**PUT Request**
```http
PUT /books/1/ HTTP/1.1
Content-Type: multipart/form-data
Authorization: Bearer <your_token>

{
    "title": "Updated Book Title",
    "author": "Updated Author Name",
    "isbn": "1234567890123",
    "publication_date": "2023-01-01",
    "publisher": "Updated Publisher Name",
    "image": <file>
}
```

**DELETE Request**
```http
DELETE /books/1/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <your_token>
```
