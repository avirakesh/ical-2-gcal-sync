from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
TOKEN_FILE_PATH = 'app_secrets/token.pickle'
CREDENTIAL_FILE_PATH = 'app_secrets/credentials.json'


def main():
    creds = None

    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_FILE_PATH, SCOPES)
            creds = flow.run_local_server(port=8085)
        with open(TOKEN_FILE_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service\
        .events()\
        .list(calendarId='primary', timeMin=now,
              maxResults=10, singleEvents=True, orderBy='startTime')\
        .execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
