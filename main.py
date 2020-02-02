from flask import Flask, request, jsonify
from calendar_helpers import calendar, currency

app = Flask(__name__)

# make basic database to store flights

# make endpoints for Google Calendar API's POST requests
# make one-time watch request on server launch to Google, specifying our post endpoint

# look into two delayed responses to one request

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/actions/RBC')
def RBC_actions():
    pass


if __name__ == '__main__':
    app.run(debug=True)
