from flask import Flask, render_template
from calendar_helpers import get_flights, flights_info_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# for the demo, we implemented the RBCs Google Calendar integration to automatically send you exchanged money when a flight is detected
@app.route('/actions/RBC')
def RBC_actions():
    flights = get_flights()
    flight_info = flights_info_string(flights)
    if not flight_info or len(flight_info) is 0:
        return "Unable to find foreign currency information :("
    return flight_info

@app.route('/confirmations/RBC')
def RBC_confirmation():
    return render_template("rbc_confirmation.html")


if __name__ == '__main__':
    app.run(debug=True)
