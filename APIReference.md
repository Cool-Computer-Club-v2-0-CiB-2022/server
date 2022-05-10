# Cool Computer Club v2.0 CiB Prototype Server API Reference

## Table of Contents  
- [Login](#login)  
- [Register](#register)  

## Login

HTTP POST /login

Request:

JSON

```json
{
    "username": case insensitive,
    "password": case sensitive
}
```

Response:

Session ID cookie and JSON

```json
{
    "username": correct case for username,
    "accessLevel": the users access level string
}
```

Response Status Codes:
- `200` - Success
- `401` - Not successful
- `422` - Invalid JSON

## Register
HTTP POST /register

Request JSON:

Session ID cookie for accound with admin or manager access level and JSON

```json
{
    "username": case sensitive,
    "password": case sensitive,
    "accessLevel": case sensitive
}
```

Response Status Codes:
- `200` - Success
- `401` - Not authorised
- `409` - User already exists
- `422` - Invalid JSON

## Access Levels

- Admin - "admin" 
  - Access everything
- Manager - "manager"
  - Access everything except account creation
- Service Desk - "serviceDesk"
  - Be able to do only service desk things
- Technician - "technician"
  - Be able to do only technician things