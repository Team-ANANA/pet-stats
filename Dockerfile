FROM python:3.8-slim-buster
WORKDIR /usr/local/src
COPY src .
CMD ["python3", "server.py"]
