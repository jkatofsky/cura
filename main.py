from flask import Flask, render_template
from calendar_helpers import get_flights, convert_to_currency_of_dest

app = Flask(__name__)

# tweak the calendar API interactions

@app.route('/')
def hello_world():
    return 'Hello, World!'

# for the demo, we implemented the RBCs Google Calendar integration to automatically send you exchanged money when a flight is detected
@app.route('/actions/RBC')
def RBC_actions():
    flights = get_flights()
    currency_info = convert_to_currency_of_dest(flights)
    if not currency_info:
        return "Unable to find foreign currency information :("
    amount, curr = currency_info
    return 'Exchange 500 CAD for %.3f %s' % (amount, curr)

@app.route('/confirmations/RBC')
def RBC_confirmation():
    return render_template("rbc_confirmation.html")


if __name__ == '__main__':
    app.run(debug=True)
