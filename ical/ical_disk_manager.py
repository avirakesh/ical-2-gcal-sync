import os
import requests
from icalendar import Calendar
from proto.calendar_pb2 import Calendar as ProtoCalendar

_ICAL_LINK_FILE = "app_secrets/ical.link"
_ICAL_DIR = "seen_icals"
_LAST_CAL_EVENTS_FILE = "last_cal.proto"

class ICalDiskManager:
    _disk_manager = None

    @staticmethod
    def init():
        pass

    @staticmethod
    def get_disk_manager():
        if ICalDiskManager._disk_manager is None:
            ICalDiskManager._disk_manager = ICalDiskManager._get_disk_manager()
        return ICalDiskManager._disk_manager

    @staticmethod
    def _get_disk_manager():
        return ICalDiskManager()

    def __init__(self):
        if not os.path.exists(_ICAL_DIR):
            os.mkdir(_ICAL_DIR)

        self._set_web_url()

    def _set_web_url(self):
        url = None
        if os.path.exists(_ICAL_LINK_FILE):
            with open(_ICAL_LINK_FILE, 'r') as link_file:
                text_contents = link_file.readlines()
                if len(text_contents) == 1:
                    url = text_contents[0].strip()

        if not url:
            url = input("iCal Link: ")
            if url.startswith("webcal://"):
                url = url[len("webcal://"):]

            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url

            with open(_ICAL_LINK_FILE, 'w') as link_file:
                link_file.writelines(url)

        self.web_url = url

    def get_latest_cal(self):
        ical = Calendar.from_ical(requests.get(self.web_url).text)
        for it in ical.walk():
            print(it)
