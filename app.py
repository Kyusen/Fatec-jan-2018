from flask import Flask
import requests, json

app = Flask(__name__)


@app.route('/')
def hello():
    first_route = requests.get('http://localhost:5000/')
    return first_route.content

if __name__ == '__main__':
    app.run(port=8000, debug=True)