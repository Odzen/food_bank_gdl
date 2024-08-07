# Server to Food Bank tickets mobile App
Rest API that handles all the logic of tickets, users, and requests for administrative purposes of the [Food Bank - Guadalajara](https://bdalimentos.org/). The endpoints of this API aim to work with any client, a web or mobile application.

# Roles
- Developer: Superadmin.
- Admin: They can approve or reject user sign-ups. They can assign tickets to users. They can manage all the tickets, users (not devs) and requests. 
- Employee: Can create and update tickets. They can see the tickets and requests assigned to them or created by them. They can create a request to the admin to authorize a process.

## Tech stack
- Python 3.12.4
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Mailgun](https://www.mailgun.com/) (for email sending)
- [AWS](https://aws.amazon.com/) (for file storage)
- [Heroku](https://www.heroku.com/) (for deployment)
- [Pytest](https://docs.pytest.org/en/stable/) (for testing)
- [SonarCloud](https://www.sonarsource.com/products/sonarcloud/) (for code quality)

## To start
1. Ask for `.env` variables, follow `.env.example` and create a local `.env` file with the correct values.
2. Create python env: `python -m venv env`
3. Activate env: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run API: `fastapi dev src/main.py`
6. Go to `http://127.0.0.1:8000/docs` to see the documentation on swagger.

## To setup de Database
Tha application works with MongoDB database, you can create your own instance in the cloud and follow the .env.example instructions to connect to it. Or run a local instance.

If you want to populate the database with some data, you can run the `src/seed/seed.py` script using `python -m src.seed.seed`

### To create a MongoDB instance in MongoDB Atlas
1. Create an account
2. Create a cluster
3. Create a database called `food-bank`

### To create a local MongoDB instance
1. Install MongoDB locally
2. Run the MongoDB service
3. Create a database called `food-bank`

## To setup 3rd party services - Mailgun
Create an account in Mailgun and get the credentials, then set them in the `.env` file. Then create templates for the emails in the Mailgun dashboard.

1. `auth-request`: Template name for the email that is sent to the admin when a user signs up and needs approval to access the app.
2. `notification-user-auth`: Template name for the email that is sent to the user when an admin approves the sign up.
3. `notify-tickets`: Template name for the email that is sent to the user is assigned to a ticket.

## To setup AWS
In this project, we use AWS S3 to store images. To use this service you need to create an account, get the credentials and set them in the `.env` file. Then you need to create a bucket and set the permissions to allow public access to the images, the bucket name should be called
`food-bank-bucket`.

## To run the tests
To run unit tests you can use `pytest` command.

## Try it out
Go to the [API documentation](https://food-bank-81fe7f521972.herokuapp.com/docs) to see the endpoints and try them out. The credentials to access the API are:

### Role: Developer
- Email: dev@example.com
- Password: dev

### Role: Admin
- Email: admin@mail.com
- Password: admin

### Role: Employee
- Email: employee@example.com
- Password: employee

