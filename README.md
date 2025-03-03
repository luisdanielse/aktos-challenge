# aktos-challenge
The main purpose of this project is to show a basic API as a part of an Interview in https://www.aktos.ai/

The core technologies used involve:
- Django
- Django Rest Framework
- PostgreSQL
- Deployment on Ubuntu and NGINX


## Main endpoints
At the current time, the application consists of two endpoints:
###http://aktos.danielsotodev.com
This endpoint will show us an HTML view with a basic form that allow us to load a CSV file.
Based on the CSV file, the database will be populated.
It is important to mention, the current design does not validate the columns provided in the CSV.

###http://aktos.danielsotodev.com/accounts
Web Service that let us retrieve information about the debts in the database.
These are the following arguments that can be sent through a GET parameter:
1. **min_balance**: The min amount to filter the data by.
2. **max_balance**: The max amount to filter the data by.
3. **consumer_name**: A query for the consumer name to filter the data by.
4. **status**: The status of the debt to filter the data by. 

####Testing endpoints:
- http://aktos.danielsotodev.com/accounts/?min_balance=50000
- http://aktos.danielsotodev.com/accounts/?min_balance=50000&status=inactive
- http://aktos.danielsotodev.com/accounts/?status=PAID_IN_FULL
