#!/bin/bash


echo 'in startup.sh, installing reqs'
pip install -r requirements.txt

export PET_STATS_PETFINDER_PAYLOAD="grant_type=client_credentials&client_id=NiCmTqdkaMK5noEjfRHZwFYrZtOkUd3NVUNKLrrapbH9u5zvJC&client_secret=WN8IH6ibwEGTi1qdNN82wlgURnz5SQZmYLRYFq71"
export PET_STATS_DB_PASSWORD="my-secret-pw"

python3 ./utils/coordinator.py