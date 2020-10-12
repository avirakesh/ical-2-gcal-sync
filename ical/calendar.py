from .ical_disk_manager import ICalDiskManager


class ICalManager:
    _manager = None

    @staticmethod
    def init():
        return ICalDiskManager.init() \
            and ICalManager.get_ical_manager() is not None

    @staticmethod
    def get_ical_manager():
        if ICalManager._manager is None:
            ICalManager._manager = ICalManager._get_ical_manager()
        return ICalManager._manager

    @staticmethod
    def _get_ical_manager():
        return ICalManager()

    def __init__(self):
        self.disk_manager = ICalDiskManager.get_disk_manager()

    def get_cal(self):
        self.disk_manager.get_latest_cal()

