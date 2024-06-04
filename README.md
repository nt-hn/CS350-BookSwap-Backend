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
4. [Chat API](#chat-api)
    - [Create Chat](#1-create-chat)
    - [Get Chats](#2-get-chats)
    - [Get Messages](#3-get-messages)
    - [Create Messages](#4-create-messages)
    - [Delete Chat](#5-delete-chat)
    - [WebSocket Usage for Chat](#websocket-usage-for-chat)
5. [Requests](#requests)
    - [Get Books Where Requests are Sent](#1-get-books-where-requests-are-sent)
    - [Get Books Where Requests are Received](#2-get-books-where-requests-are-received)
    - [Get Books Where Requests are Ongoing](#3-get-books-where-requests-are-ongoing)

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
    - `genre`: String(Optional: will default to Fiction)
    - `isPrivate`: Boolean(Optional: will default to False)

#### Responses
- `200 OK`: A list of all books (for `GET`).
- `201 Created`: The created book object (for `POST`).
- `400 Bad Request`: Validation errors.
- `403 Forbidden`: Authentication credentials not provided.

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
    "image": <file>
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
- **Authentication required**: Yes (Only the owner of the book is able to update)
- **Request body**:
    - `title`: String (optional)
    - `author`: String (optional)
    - `isbn`: String (optional)
    - `publication_date`: String (optional, format: 'YYYY-MM-DD')
    - `publisher`: String (optional)
    - `image`: File (optional)
    - `current_owner`: Will by default be the user currently authenticated
  - Note for `title`, `author`, `isbn`, `publication_date`, and `publisher` make sure you have the previous information in place. Otherwise, the field will be saved empty. Image file will by default be the previous one unless updated.

#### Request (DELETE)
- **Authentication required**: Yes (Only the owner of the book is able to delete)

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
### Search Book by Title and Author

Endpoint: `/book/search_book_by_title_and_author/`

#### Request (POST)

#### Request Parameters
- **Request Body**:
  - `author` (string, required if title not provided): The name of the author to search for.
  - `title` (string, required if author not provided): The title of the book to search for (required).

#### Example Request
**URL**: `/book/search_book_by_title_and_author/`

**Request Body**:
```json
{
  "author": "J.K. Rowling"
}
```

#### Responses
- **200 OK**: Returns a list of books matching the search criteria.
  ```json
  [
    {
      "id": 1,
      "title": "Harry Potter and the Philosopher's Stone",
      "author": "J.K. Rowling",
      "isbn": "9780747532743",
      "publication_date": "1997-06-26",
      "publisher": "Bloomsbury",
      "current_owner": 1
    },
    {
      "id": 2,
      "title": "Harry Potter and the Chamber of Secrets",
      "author": "J.K. Rowling",
      "isbn": "9780747538486",
      "publication_date": "1998-07-02",
      "publisher": "Bloomsbury",
      "current_owner": 1
    }
  ]
  ```
- **400 Bad Request**: Returns an error if neither `title` nor `author` is provided.
  ```json
  {
    "Error": "At least one of title or author parameters is required"
  }
  ```

---

## Chat API

#### 1. Create Chat
End point: `/chat/create_chat/`
- **Method**: `POST`
- **Authentication**: Required

**Request Body**:
- `chat_member_2` (integer): user_id of the other chat member.

**Responses**:
- **201 Created**: Returns the created chat object.
- **400 Bad Request**: Returns validation errors.
- **403 Forbidden**: Returns if the user is not authenticated.

#### 2. Get Chats
End point: `/chat/get_chats/`
- **Method**: `GET`
- **Authentication**: Required

**Responses**:
- **200 OK**: Returns a list of chats involving the authenticated user.
- **403 Forbidden**: Returns if the user is not authenticated.

#### 3. Get Messages
End point: `/chat/get_messeges/<int:chat_id>/`
- **Method**: `GET`
- **Authentication**: Required

**URL Parameters**:
- `chat_id` (integer): ID of the chat.

**Responses**:
- **200 OK**: Returns a list of messages for the specified chat.
- **403 Forbidden**: Returns if the user is not authenticated.

#### 4. Create Messages
End point: `/chat/create_messages/<int:chat_id>/`
- **Method**: `POST`
- **Authentication**: Required

**URL Parameters**:
- `chat_id` (integer): ID of the chat.

**Request Body**:
- `message` (string): The text of the message.

**Responses**:
- **200 OK**: Returns the updated list of messages for the specified chat.
- **400 Bad Request**: Returns validation errors or other issues.
- **403 Forbidden**: Returns if the user is not authenticated.

### Example Responses

**Create Chat - Success**:
```json
{
    "chat_member_1": 1,
    "chat_member_2": 2,
}
```

**Get Chats - Success**:
```json
[
    {
        "chat_member_1": 1,
        "chat_member_2": 2,
    },
    {
        "chat_member_1": 1,
        "chat_member_2": 3,
    }
]
```

**Get Messages - Success**:
```json
[
    {
        "chatroom": 1,
        "user": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe"
          },
        "time": "2023-05-20T14:55:00Z",
        "text": "Hello!"
    },
    {
        "chatroom": 1,
        "user": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe"
          },
        "time": "2023-05-20T14:56:00Z",
        "text": "How was your day?"
    }
]
```

**Create Messages - Success**:
```json
[
    {
        "chatroom": 1,
        "user": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe"
          },
        "text": "Hello!",
        "time": "2023-05-20T14:55:00Z"
    },
    {
        "chatroom": 1,
        "user": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe"
          },
        "text": "How was your day?",
        "time": "2023-05-20T14:56:00Z"
    },
    {
        "chatroom": 1,
        "user": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe"
          },
        "text": "How are you?",
        "time": "2023-05-20T14:57:00Z"
    }
]
```

#### 5. Delete Chat
End point: `/chat/delete_chat/<int:chat_id>/`
- **Method**: `DELETE`
- **Authentication**: Required

**URL Parameters**:
- `chat_id` (integer): ID of the chat.

**Responses**:
- **204 No Content**: Chat successfully deleted.
- **400 Bad Request**: Invalid request method (not DELETE).
- **403 Forbidden**: Authentication credentials were not provided.

### Example Usage
To delete a chat with ID `123`:

1. **HTTP Method**: DELETE
2. **URL**: `/chat/delete_chat/123/`
3. **Response**: 204 No Content

## WebSocket Usage for Chat

### WebSocket URL
```javascript
const chatSocket = new WebSocket(
    `ws://${backend_host}/ws/chat/${chatroom_id}/`
);
```

### Example Usage
  ```javascript
  const chatSocket = new WebSocket(
    `ws://${backend_host}/ws/chat/${chatroom_id}/`
  );
  chatSocket.onmessage = (e) => {
    //TODO: put the logic for sending message here
  };

  chatSocket.onclose = (e) => {
      //TODO: put the logic for what to do when connection is closed here
  };
  
  chatSocket.send(
    //TODO: put the logic for what to do when sending message between connected sockets here
  );
  ```

### Usage
- **Initialize WebSocket**: Establishes a WebSocket connection (`handshake`) to the server.
- **Receive Messages**: Handles incoming messages pereferably used for updating chat interface.
- **Send Messages**: Sends messages to the server using WebSocket.

**Note**: This setup enables real-time communication in the chat room using WebSockets.

----
### Requests

### 1. Get Books Where Requests are Sent

#### Endpoint
**GET** `/book_request/sent/`

#### Description
Retrieve books where the authenticated user has sent requests.

#### Responses
- **200 OK**: Returns a list of books where requests are sent by the authenticated user.
- **403 Forbidden**: Authentication credentials were not provided.

### 2. Get Books Where Requests are Received

#### Endpoint
**GET** `/book_request/received/`

#### Description
Retrieve books where the authenticated user has asked for.

#### Responses
- **200 OK**: Returns a list of books where requests are received by the authenticated user.
- **403 Forbidden**: Authentication credentials were not provided.

### 3. Get Books Where Requests are Ongoing

#### Endpoint
**GET** `/book_request/ongoing/`

#### Description
Retrieve books where the authenticated user is involved in ongoing requests.

#### Responses
- **200 OK**: Returns a list of books where requests are ongoing for the authenticated user.
- **403 Forbidden**: Authentication credentials were not provided.

### Note
- Ensure that authentication credentials are provided to access the endpoints.
