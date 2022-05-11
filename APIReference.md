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

```json
{
    "username": case sensitive,
    "password": case sensitive,
    "accessLevel": case sensitive
}
```

Response Status Codes:
- `200` - Success
- `409` - User already exists
- `422` - Invalid JSON

## New Asset

HTTP POST [/asset/new](https://api.cool-computer-club.com/asset/new)

Request:

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
- `422` - Invalid JSON

## Get Asset

HTTP GET [/asset/get/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/get/00000000-0000-0000-0000-000000000000)

Request:

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
- `404` - Asset not found

## Edit Asset

HTTP PUT [/asset/edit/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/edit/00000000-0000-0000-0000-000000000000)

Request:

JSON of the data that has been changed

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
- `404` - Not found
- `422` - Invalid JSON

## Delete Asset

HTTP DELETE [/asset/delete/\<assetInventoryNumber>](https://api.cool-computer-club.com/asset/delete/00000000-0000-0000-0000-000000000000)

Request:

assetInventoryNumber must be in the url

note: does not check if the asset exists, deleting an asset that doesnt exist will do nothing and respond with 200

Response Status Codes:
- `200` - Success

## Generate Report

HTTP GET [/report.\<format>](https://api.cool-computer-club.com/report.json)

Supported formats are JSON and CSV (`/report.json` and `/report.csv`). If no format is provided, response will be a list of tuples, the output of sqlite3, converted to string with no formatting (`/report`, not recommended).

Request:

The projection, restriction, and order can be specified in the URL query string

Projection:

The showFields parameter must be a list of the fields that are to be included in the report. Case sensitive. By default will show everything.

```
https://api.cool-computer-club.com/report.json
?showFields=[assetName,type,status]
```

Restriction:

The query key must be the field name and the query value must be what to check it against. By default there is no restriction, multiple restrictions can be used and will be applied as an AND.

```
Show only assets that are installed:
https://api.cool-computer-club.com/report.json
?status="Installed"
Show only assets that are installed and in an office:
https://api.cool-computer-club.com/report.json
?status="Installed"&locationType="Office"
```

Sorting:

Use the orderBy parameter with the field as the value, by default will sort by assetInventoryNumber ascending. Add _desc to the end to sort by descending.

```
Sort by status ascending:
https://api.cool-computer-club.com/report.json
?orderBy=status
or:
https://api.cool-computer-club.com/report.json
?orderBy=status_asc

Sort by status descending:
https://api.cool-computer-club.com/report.json
?orderBy=status_desc
```

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

## Access Levels

- Manager - "manager"
  - Access everything
- Service Desk - "serviceDesk"
  - Be able to do only service desk things
- Technician - "technician"
  - Be able to do only technician things