from gcal.calendar import SelectedCalProvider
from ical.calendar import ICalManager


def init_components():
    SelectedCalProvider.init()
    ICalManager.init()


def main():
    init_components()

    ICalManager.get_ical_manager().get_cal()


if __name__ == '__main__':
    main()
