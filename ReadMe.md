## **URL Scanner using Python**
This project is used as lookup for the URL that is passed and verified against the
known list of malicious URL's in DB. This project has various CRUD operation for records in database

### **Setting up the project**

#### Requirements:

    1. Python 3.7
    2. MySQL

Please refer the requirements.txt file for Python dependecies. Make sure that all the dependencies are met before runnig the project
for running the requirements.txt.

All configurations are configured in config.ini

`All DB related config should go below DB_CONFIG and Flask related settings to FLASK_APP. For flask only port needs to be configured and for DB Hostname, User, Password and DB Name. This will be consumed in the program.`

Here are the sequence of commands to be executed in a clean RHEL 8 VM to run this project.

1. Install Python 3.x : 
``` yum install python3 ```
3. Extract project tar : 
``` tar xvf urlScanner_latest.tar ```
5. Go to extracted folder : 
``` cd urlScanner_latest/ ```
7. Install all dependencies : 
``` pip3 install -r requirements.txt ```
9. To Install MySQL, execute following commands in order :
      ```
      rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
      sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo
      yum module disable mysql
      yum --enablerepo=mysql80-community install mysql-community-server
      service mysqld status
      service mysqld start
      service mysqld status
      grep "A temporary password" /var/log/mysqld.log
      ```
      [ for the following command, give temp password for root, change the root password, and give "y" to all 4 questions]
      - mysql_secure_installation

      ``` mysql_secure_installation ```

      Securing the MySQL server deployment.

      Enter password for user root:
      Change the password for root ? ((Press y|Y for Yes, any other key for No) : y

      Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
      Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
      Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
      Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y

      ``` service mysqld restart ```

  6. To setup database, execute the following commands and provide DB root user password when prompted.
      ``` 
      mysql -u root -p -e "show databases;" 
      mysql -u root -p -e "CREATE DATABASE urlscanner1;"
      mysql -u root -p -e "show databases;" 
      mysql -u root -p -e "use urlscanner; show tables;" 
      mysql -u root -p -e "CREATE TABLE url_db (     id int NOT NULL AUTO_INCREMENT,     URL varchar(10000) NOT NULL,     PRIMARY KEY (id) );" 
      mysql -u root -p -e "show tables;" 
      mysql -u root -p -e "use urlscanner; select * from url_db;" 
      ```

7. Update config.ini with the username/password
8. To run UT cases : 
   ``` python3 -m unittest unit.MyTestCase ```
10. Run the urlScanner app : 
    ``` python3 main.py ```
12. To run automated FT cases
13. To run FT cases manually to test REST API calls and output :

App Check

``` curl http://localhost:3200/ ```

Sample Response:

Fetch all records:

``` curl http://localhost:3200/rest/api/v1/urlScanner/all  ```

Sample Response:

[{"id": 1, "URL": "http://10.10.10.10:9000/test/urlmalware"}, {"id": 2, "URL": "http://10.10.10.10:9000/test/scanner"},
{"id": 3, "URL": "http://10.120.34.12/failure/test"}, {"id": 5, "URL": "http://10.10.10.10:9000/test/urlmalware"}]

Insert a record:
URL should be sent in as form data with key as insert_url. The URL will be directly inserted without any validation.

``` curl -X POST http://localhost:3200/rest/api/v1/urlScanner/add -H "Content-Type: application/x-www-form-urlencoded" -d "insert_url=https://www.malware.com/test" ```
Sample Response:


    
Update a record :

``` PUT http://localhost:8100/rest/api/v1/urlScanner/<id> ```

Send the updated url as part of form data with key as update_url and the id in the request url.

Delete a record:

``` DELETE http://localhost:8100/rest/api/v1/urlScanner/<id> ```

    
For Malicious url look up:

``` curl --location --request GET 'http://localhost:3200/rest/api/v1/urlScanner/isSafeUrl?hostname=https://www.malware.com&originalpathquerystring=/test' ```

Sample Response:
Fetch record for specific id:

``` GET http://localhost:8100/rest/api/v1/urlScanner/<id> ```

Hostname, Port (optional) and Query Path should be sent as named query parameter after encoding. The service will decode and process the data further.

Positive response : Status 200, The Url is clean

Negative response : Status 400, The URL is unsafe

Exception : Status 200, Exception occured in dblayer

