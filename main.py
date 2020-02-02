from flask import Flask, render_template
from calendar_helpers import get_flights, flights_info_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# for the demo, we implemented the RBCs Google Calendar integration to automatically send you exchanged money when a flight is detected
@app.route('/actions/RBC/currency')
def RBC_action_currency():
    flights = get_flights()
    flight_info = flights_info_string(flights)
    if not flight_info or len(flight_info) is 0:
        return "Unable to find foreign currency information :("
    return flight_info

@app.route("/actions/RBC/cancel")
def RBC_action_cancel():
    return "Due to your upcomming flight, <br> we won't cancel your card abroad."

@app.route('/confirmations/RBC/currency')
def RBC_confirmation_currency():
    return render_template("rbc_confirmation.html")


if __name__ == '__main__':
    app.run(debug=True)
