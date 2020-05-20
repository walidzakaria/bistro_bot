from time import sleep
from controller import search_hotel_only, scan_for_data, click_location, wait_for_update, get_starting_position
from models import StaticVariables, ComparisonRecord
from stores import get_last_record, get_record, save_record, save_work


def main():
    start_up()
    go_hotel_only()
    end_app()


def go_hotel_only():
    print(f'number of rows: {StaticVariables.last_record - 3}')
    for i in range(4, StaticVariables.last_record + 1):
        StaticVariables.current_record = i
        row_record = get_record(i)
        print(row_record)
        result = search_hotel_only(row_record)
        print(result)
        if result:
            row_record = scan_for_data(row_record)
            save_record(row_record)
            save_work()


def start_up():
    # Countdown timer
    print("Starting", end="")
    for i in range(0, 3):
        print(".", end=".")
        sleep(1)
    print('reading input Excel data...')
    get_last_record()
    print('GO!')


def end_app():
    save_work()
    exit(0)
    print("Go")


if __name__ == '__main__':
    main()
