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

def space_delim_list_strs(list):
    string = ""
    for elem in list:
        string += " %s " % str(elem)
    return string

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
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    flights = []
    for event in events:
        if event['summary'].lower().startswith('flight to'):
            flights.append(event)
    for event in flights:
        start = event['start'].get('dateTime')
        startDate = start[0:10]
        startTime = start[11:19]
        destination = event['summary'].split()
        destination = space_delim_list_strs(destination[2:])
        flights_formatted.append((startDate, startTime, destination))

    return flights_formatted

def flights_info_string(flights_formatted):

    string = ""

    for flight in flights_formatted:
        if not flight[2] == 'Montreal':

            string += "Flight to %s on %s. " % (flight[2], flight[0])

            query = "%s currency to CAD xe" % flight[2]

            for website in search(query, tld="ca", num=20, stop=20):
                if website[12:18] == 'xe.com':
                    currency = website[website.index('From') + 5: website.index('From') + 8]
                    if not currency == 'CAD':
                        amount, curr = currency_converter(currency)
                        string += "Exchange 500 CAD for %.3f %s?" % (amount, curr)
                    else:
                        currency = website[website.index('To') + 3: website.index('To') + 6]
                        if not currency == 'CAD':
                            amount, curr = currency_converter(currency)
                            string += "We can exchange 500 CAD for %.3f %s\n" % (amount, curr)
                    break
    return string

def currency_converter(currency):
    cur_conv = CurrencyConverter()
    amount = cur_conv.convert(500, 'CAD', currency)
    return (amount, currency)
