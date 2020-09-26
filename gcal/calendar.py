from .service import ServiceProvider
import os.path

_SELECTED_CALENDAR_FILE_PATH = 'app_secrets/selected.calendar'


class SelectedCalProvider:
    _selected_calendar = None

    @staticmethod
    def _get_selected_calendar():
        service = ServiceProvider.get_authenticated_service()
        page_token = None
        calendars = {}
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendar_id = calendar_list_entry['id']
                calendar_summary = calendar_list_entry['summary']
                calendars[calendar_id] = calendar_summary
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        if len(calendars) == 0:
            print('Couldn\'t find calendars')
            return None

        selected_calendar = None
        if os.path.exists(_SELECTED_CALENDAR_FILE_PATH):
            with open(_SELECTED_CALENDAR_FILE_PATH, 'r') as cal:
                file_content = cal.readlines()
                if len(file_content) == 1:
                    selected_id = file_content[0].strip()
                    if selected_id in calendars:
                        selected_calendar = selected_id

            if not selected_calendar:
                print('Could not find selected calendar.')
                print('Ensure that ' + _SELECTED_CALENDAR_FILE_PATH + ' contains a valid calendar ID')

        return selected_calendar

    @staticmethod
    def get_selected_calendar():
        if not SelectedCalProvider._selected_calendar:
            SelectedCalProvider._selected_calendar = SelectedCalProvider._get_selected_calendar()
        return SelectedCalProvider._selected_calendar
