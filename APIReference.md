# Cool Computer Club v2.0 CiB Prototype Server API Reference

## Table of Contents  
- [Login](#login)  
- [Register](#register)  
- Assets
  - [New Asset](#new-asset)

## Login

HTTP POST [/login](https://api.cool-computer-club.com/login)

Request:

Username and password in a JSON

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
HTTP POST [/register](https://api.cool-computer-club.com/register)

Request:

Session ID cookie for accound with manager access level and JSON

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

## New Asset

HTTP POST [/asset/new](https://api.cool-computer-club.com/asset/new)

Request:

Session ID cookie for accound with manager or technician access level and JSON

Only assetName is required, everything else is optional

Everything is currently stored as VARCHAR but this may change

```json
{
    "assetName": "",
    "type": "",
    "typePresence": "",
    "location": "",
    "locationCode": "",
    "locationType": "",
    "resolverQueue": "",
    "status": "",
    "subStatus": "",
    "assignedTo": "",
    "billedTo": "",
    "dateCreated": "",
    "dateActive": "",
    "dateInstalled": "",
    "dateDecomm": "",
    "maintenanceWindow": ""
}
```

Response:

Returns a UUID4 for the inventory number

```json
{
    "assetInventoryNumber": "00000000-0000-0000-0000-000000000000",
}
```

Response Status Codes:
- `200` - Success
- `401` - Not authorised
- `422` - Invalid JSON

## Access Levels

- Manager - "manager"
  - Access everything
- Service Desk - "serviceDesk"
  - Be able to do only service desk things
- Technician - "technician"
  - Be able to do only technician things