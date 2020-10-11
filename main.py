from gcal.calendar import SelectedCalProvider
from gcal.service import ServiceProvider

def init_components():
    ServiceProvider.init()
    SelectedCalProvider.init()

def main():
    init_components()

    print(SelectedCalProvider.get_selected_calendar())


if __name__ == '__main__':
    main()