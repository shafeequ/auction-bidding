# auction-bidding
auction and bidding system very intutive and very simple , allows multiple times to bid and take the latest bid from each bidder


# prerequiste Some basic libs/frameworks required
```
pip install tornado
pip install mysql-connector
pip install pytest, simplejson
```

# Application Setup
- move the src folder to your desired location
- install the above frameworks and libs
- setup the mysql and set up the schema from the file src/schemas/setup.sql   (change the DB name )
- configure the details of DB user name, passwd, db name and host in the sr/app_constants.py file
- run the aplication  python app.py --port=8082   ( you can specify the port as per your wish)
- access the REST APIs as exposed and mentioned in the swagger/postman collection shared

# Exposed REST API Postman Collection
src/postman
