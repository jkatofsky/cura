from flask import Flask, request, jsonify

app = Flask(__name__)

# make endpoints for the chrome extension's GET requests
# make an integration between Michael's code and my server
# make endpoints for Google Calendar API's POST requests

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
