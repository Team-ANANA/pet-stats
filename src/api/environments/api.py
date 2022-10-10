from flask import Flask

app = Flask(__name__)

@app.route('/')
def default_route():
    return 'This is the root directory. Try out the /hello route!'

@app.route('/hello')
def hello():
    return 'Hello, World!'
