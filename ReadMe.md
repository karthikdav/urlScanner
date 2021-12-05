## **URL Scanner using Python**
This project is used as lookup for the URL that is passed and verified against the 
known list of malicious URL's in DB. This project has various CRUD operation for records in database

### **Setting up the project**

#### Requirements:
    
    1. Python 3.7
    2. MySQL

Please refer the requirements.txt file for Python dependecies. Make sure that all the dependencies are met before runnig the project
for running the requirements.txt.

use command pip install -r requirements.txt

All configurations are configured in config.ini 

`All DB related config should go below DB_CONFIG and Flask related settings to FLASK_APP. For flask only port needs to be configured and for DB Hostname, User, Password and DB Name. This will be consumed in the program.`

once above steps are done execute main.py

### **API's available**
Fetch all records:

GET http://localhost:8100/rest/api/v1/urlScanner/all

Sample Response:

[{"id": 1, "URL": "http://10.10.10.10:9000/test/urlmalware"}, {"id": 2, "URL": "http://10.10.10.10:9000/test/scanner"},
{"id": 3, "URL": "http://10.120.34.12/failure/test"}, {"id": 5, "URL": "http://10.10.10.10:9000/test/urlmalware"}]

Fetch record for specific id:

GET http://localhost:8100/rest/api/v1/urlScanner/<id>

Insert a record:

POST http://localhost:8100/rest/api/v1/urlScanner/add

`URL should be sent in as form data with key as insert_url. The URL will be directly inserted without any validation.`

Update a record :

PUT http://localhost:8100/rest/api/v1/urlScanner/<id>

`Send the updated url as part of form data with key as update_url and the id in the request url.`

Delete a record:

DELETE http://localhost:8100/rest/api/v1/urlScanner/<id>

For Malicious url look up:

GET http://localhost:8100/rest/api/v1/urlScanner/isSafeUrl

`Hostname, Port (optional) and Query Path should be sent as named query parameter after encoding. The service will decode and process the data further.`

Positive response : Status 200, The Url is clean

Negative response : Status 400, The URL is unsafe

Exception : Status 200, Exception occured in dblayer
