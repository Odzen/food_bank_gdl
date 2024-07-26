# Server to Food Bank tickets mobile App
Rest API that handles all the logic of tickets, users, and requests for administrative purposes of the [Food Bank - Guadalajara](https://bdalimentos.org/). The endpoints of this API aim to work with any client, a web or mobile application.

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

## To run the tests
To run unit tests you can use `pytest` command.

