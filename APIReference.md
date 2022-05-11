# Cool Computer Club v2.0 CiB Prototype Server API Reference

## Table of Contents  
- [Login](#login)  
- [Register](#register)  
- Assets
  - [New Asset](#new-asset)
  - [Get Asset](#get-asset)
  - [Edit Asset](#edit-asset)
  - [Delete Asset](#delete-asset)
- [Generate Report](#generate-report) 

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

assetInventoryNumber will be auto generated if not included or is already in the system

Everything is currently stored as VARCHAR but this may change

```json
{
    "assetInventoryNumber": "",
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

Returns the inventory number, UUID4 if auto generated

```json
{
    "assetInventoryNumber": "00000000-0000-0000-0000-000000000000",
}
```

Response Status Codes:
- `200` - Success
- `401` - Not authorised
- `422` - Invalid JSON

## Get Asset

HTTP GET [/asset/get/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/get/00000000-0000-0000-0000-000000000000)

Request:

Session ID cookie, any access level

assetInventoryNumber must be in the url

Response:

```json
{
    "assetInventoryNumber": "",
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

Response Status Codes:
- `200` - Success
- `401` - Not authorised
- `404` - Asset not found

## Edit Asset

HTTP PUT [/asset/edit/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/edit/00000000-0000-0000-0000-000000000000)

Request:

Session ID cookie for accound with manager or technician access level and JSON of the data that has been changed

assetInventoryNumber can not be changed, everything else can

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

Response Status Codes:
- `200` - Success
- `401` - Not authorised
- `404` - Not found
- `422` - Invalid JSON

## Delete Asset

HTTP DELETE [/asset/delete/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/delete/00000000-0000-0000-0000-000000000000)

Request:

Session ID cookie of admin or technician access level

assetInventoryNumber must be in the url

note: does not check if the asset exists, deleting an asset that doesnt exist will do nothing and respond with 200

Response Status Codes:
- `200` - Success
- `401` - Not authorised

## Generate Report

HTTP GET [/report.\<format>](https://api.cool-computer-club.com/report.json)

Filtering the reports is currently not implemented, I am working on it at the moment

Supported formats are JSON and CSV (`/report.json` and `/report.csv`). If no format is provided, response will be a list of tuples, the output of sqlite3, converted to string with no formatting (`/report`, not recommended).

Request:

A session ID cookie of any access level

JSON response:

A dict with a list of dicts in the same format of [Get Asset](#get-asset)

```json
{
    "data": [ -- list of dicts -- ],
    "query": "-- the SQL query used (for debugging) --"
}
```

CSV response:

A file with the same data but in csv format

Response Status Codes:
- `200` - Success
- `401` - Not authorised

## Access Levels

- Manager - "manager"
  - Access everything
- Service Desk - "serviceDesk"
  - Be able to do only service desk things
- Technician - "technician"
  - Be able to do only technician things