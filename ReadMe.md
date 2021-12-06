## **URL Scanner using Python**
This project is used as lookup for the URL that is passed and verified against the known list of malicious URL's in DB. 
This project has various CRUD operation for records in database

### **Setting up the project**

You can achieve the following by executing the given commands in order.
-	No other tools required except a RHEL 8 VM and internet access.
-	Setup Python 3.x if not already present
-	Install all dependencies for the project
-	Setup MySQL, create tables and configure the DB config into the project
-	Bring up the project into running state
-	Execute all UT cases for DB layer
-	Execute all automated FT [functional test] cases for the REST API
-	Execute all FT [functional test] cases for the REST API using Curl


#### Requirements:

    1. Python 3.7
    2. MySQL

- Please refer the requirements.txt file for Python dependecies. 
- Make sure that all the dependencies are met before runnig the project for running the requirements.txt.
- All configurations are configured in config.ini
- All DB related config should go below DB_CONFIG and Flask related settings to FLASK_APP. 
- For flask only port needs to be configured and for DB Hostname, User, Password and DB Name. This will be consumed in the program.

#### Here are the sequence of commands to be executed in a clean RHEL 8 VM to run this project.

##### 1. Install Python 3.x : 
``` yum install python3 ```
##### 2. Extract project tar : 
``` tar xvf urlScanner_latest.tar ```
##### 3. Go to extracted folder : 
``` cd urlScanner_latest/ ```
##### 4. Install all dependencies : 
``` pip3 install -r requirements.txt ```
##### 5. To Install MySQL, execute following commands in order :
      
      rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
      sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo
      yum module disable mysql
      yum --enablerepo=mysql80-community install mysql-community-server
      service mysqld status
      service mysqld start
      service mysqld status
      grep "A temporary password" /var/log/mysqld.log
      
      [ for the following command, give temp password for root, change the root password, and give "y" to all 4 questions]
      
      
      > mysql_secure_installation
      
      Securing the MySQL server deployment.

      Enter password for user root:
      Change the password for root ? ((Press y|Y for Yes, any other key for No) : y

      Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
      Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
      Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
      Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y

      Restart MYSQL : service mysqld restart

 ##### 6. To setup database, execute the following commands and provide DB root user password when prompted.
       
      mysql -u root -p -e "show databases;" 
      mysql -u root -p -e "CREATE DATABASE urlscanner1;"
      mysql -u root -p -e "show databases;" 
      mysql -u root -p -e "use urlscanner; show tables;" 
      mysql -u root -p -e "CREATE TABLE url_db ( id int NOT NULL AUTO_INCREMENT, URL varchar(10000) NOT NULL, PRIMARY KEY (id) );" 
      mysql -u root -p -e "show tables;" 
      mysql -u root -p -e "use urlscanner; select * from url_db;" 
      

##### 7. Update config.ini with the username/password
```
[FLASK_APP]
port=3200

[DB_CONFIG]
host=127.0.0.1
user=root
password=admin
database=urlscanner
```
##### 8. To run UT cases : 
``` python3 -m unittest unit.MyTestCase ```
##### 9. Run the urlScanner app 
``` python3 main.py ```
##### 10. Open another terminal for the server and run automated FT cases
``` python3 -m unittest api_test.AppUnitTest ```
##### 11. Open another terminal for the server and run FT cases manually to test REST API calls and output 

- App Check
``` curl http://localhost:3200/ ```
  - Sample Response:
``` URL Scanner is running on port 3200 ```

- To Insert a record, URL should be sent in as form data with key as insert_url. The URL will be directly inserted without any validation.
``` curl -X POST http://localhost:3200/rest/api/v1/urlScanner/add -H "Content-Type: application/x-www-form-urlencoded" -d "insert_url=https://www.malware.com/test" ```
  - Sample Response:
``` the insert_url is https://www.malware.com/test ```

- Fetching record for specific id:
``` curl -X GET http://localhost:3200/rest/api/v1/urlScanner/1 ```
  - Sample Response:
``` [{"id": 1, "URL": "https://www.malware.com/test"} ```

- Fetch all records:
``` curl http://localhost:3200/rest/api/v1/urlScanner/all  ```
  - Sample Response:
``` [{"id": 1, "URL": "https://www.malware.com/test"}] ```


- To Update a record, send the updated url as part of form data with key as update_url and the id in the request url.
``` curl -X PUT http://localhost:3200/rest/api/v1/urlScanner/1 -H "Content-Type: application/x-www-form-urlencoded" -d "update_url=https://www.malware.com/tested" ```
  - Sample Response:
``` url id with 1 is updated with url string https://www.malware.com/tested ```

- Delete a record:
``` curl -X DELETE http://localhost:3200/rest/api/v1/urlScanner/1 ```
  - Sample Response:
``` url id with 1 is Deleted ```
    
- For Malicious url look up:
``` curl --location --request GET 'http://localhost:3200/rest/api/v1/urlScanner/isSafeUrl?hostname=https://www.malware.com&originalpathquerystring=/test' ```
  - Sample Response:
``` The URL is unsafe ```
    - hostname, port (optional) and originalpathquerystring should be sent as named query parameter after encoding. 
    - The service will decode and process the data further.
    - Positive response : Status 200, The Url is clean
    - Negative response : Status 400, The URL is unsafe
    - Exception : Status 200, Exception occured in dblayer

