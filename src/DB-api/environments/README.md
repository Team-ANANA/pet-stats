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

`sudo start.sh`

## Testing
To run unit tests, go into the virtual environment as mentioned above, then run:

`sudo run_test.sh`
