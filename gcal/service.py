from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

_SCOPES = ['https://www.googleapis.com/auth/calendar']
_TOKEN_FILE_PATH = 'app_secrets/token.pickle'
_CREDENTIAL_FILE_PATH = 'app_secrets/credentials.json'


class ServiceProvider:
    _service = None

    @staticmethod
    def get_authenticated_service():
        if not ServiceProvider._service:
            ServiceProvider._service = ServiceProvider._get_authenticated_service()
        return ServiceProvider._service

    @staticmethod
    def _get_authenticated_service():
        """
        Get OAuth tokens and creates a service for furthur API calls
        :return: A service object that can be used to make further calls API calls
        """
        creds = None

        if os.path.exists(_TOKEN_FILE_PATH):
            with open(_TOKEN_FILE_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(_CREDENTIAL_FILE_PATH, _SCOPES)
                creds = flow.run_local_server(port=8085)
            with open(_TOKEN_FILE_PATH, 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service
