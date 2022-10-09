# BACKEND API

## Introduction
This module contains the flask api server which is the backend of the pet-stats web app.

## How to run the server
To run the code locally, you need to first create a python virtual environment with the following command:

`python3 -m venv venv`

then we can enter the local virtual environment with:

`source venv/bin/activate`

within the virtual environment, install the required packages by running:

`pip install -r requirements.txt`

finally, start the flask api server by running:

`flask run`

you might need to specify the host and port by running this instead:

`flask run --host 0.0.0.0 --port 5000`
