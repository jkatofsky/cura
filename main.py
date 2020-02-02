from flask import Flask, request, jsonify, render_template
from calendar_helpers import calendar, currency

app = Flask(__name__)

# tweak the calendar API interactions

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/actions/RBC')
def RBC_actions():
    flights = calendar()
    currency_info = currency(flights)
    if not currency_info:
        return "Unable to find foreign currency information :("
    amount, curr = currency_info
    return 'Exchange 500 CAD for %.3f %s' % (amount, curr)

@app.route('/confirmations/RBC')
def RBC_confirmation():
    return render_template("rbc_confirmation.html")


if __name__ == '__main__':
    app.run(debug=True)
