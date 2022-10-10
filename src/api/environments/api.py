from flask import Flask

app = Flask(__name__)

@app.get('/')
def default_route():
    return 'This is the root directory. Try out the /hello route!'

@app.get('/hello')
def hello():
    return 'Hello, World!'
