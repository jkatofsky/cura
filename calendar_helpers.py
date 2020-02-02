from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from currency_converter import CurrencyConverter
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def get_flights():

    creds = None
    flights_formatted = []

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
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming flights')
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
        flights_formatted.append((startDate, startTime, destination))

    return flights_formatted

def convert_to_currency_of_dest(flights_formatted):
    for flight in flights_formatted:
        if not flight[2] == 'Montreal':
            print('We saw you are flying to ' + flight[2] + ' on ' + flight[0] + ' at ' + flight[1])
            print('Do you want to order foreign currency for the flight to ' + flight[2])
            query = flight[2] + " currency to CAD xe"

            for website in search(query, tld="ca", num=20, stop=20):
                if website[12:18] == 'xe.com':
                    currency = website[website.index('From') + 5: website.index('From') + 8]
                    if not currency == 'CAD':
                        return currency_converter(currency)
                    else:
                        currency = website[website.index('To') + 3: website.index('To') + 6]
                        if not currency == 'CAD':
                            return currency_converter(currency)
                    break

def currency_converter(currency):
    print(currency)
    cur_conv = CurrencyConverter()
    amount = cur_conv.convert(500, 'CAD', currency)
    return (amount, currency)
