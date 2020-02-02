from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from currency_converter import CurrencyConverter

import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly/watch']
## https://www.googleapis.com/apiName/apiVersion/resourcePath/watch
## @app.route('/calendar_demo', methods=['GET', 'POST', 'DELETE', 'PATCH'])


flights_formatted = []

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming flights', file=sys.stderr)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    flights = []
    for event in events:
        if event['summary'].startswith('Flight to'):
            flights.append(event)
    if not flights:
        print('No flights found')
    for event in flights:
        start = event['start'].get('dateTime')
        startDate = start[0:10]  # event['start'].get('date'))
        startTime = start[11:19]
        destination = event['summary'].split()
        destination = destination[2]
        flights_formatted.append([startDate, startTime, destination])
        print (startDate, startTime, destination)

def currency():
    for flight in flights_formatted:
        if not flight[2] == 'Montreal':
            print('We saw you are flying to ' + flight[2] + ' on ' + flight[0] + ' at '+ flight[1])
            print('Do you want to order foreign currency for the flight to ' + flight[2])
            query = flight[2] + " currency to CAD"
            for website in search(query, tld="ca", num=7, stop=7):
                if website[12:18] == 'xe.com':
                    currency = website[website.index('From')+5 : website.index('From')+8]
                    if not currency == 'CAD':
                        currency_converter(currency)
                    else:
                        currency = website[website.index('To')+3 : website.index('To')+6]
                        if not currency == 'CAD':
                            currency_converter(currency)
                break

def currency_converter(currency):
        print(currency)
        cur_conv = CurrencyConverter()
        amount = cur_conv.convert(500, 'CAD', currency)
        print('We can exchange 500 CAD for %.3f %s automatically.' %(amount, currency))
