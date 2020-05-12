from time import sleep
from controller import search_hotel_only, scan_for_data, click_location, wait_for_update, get_starting_position


def main():
    start_up()
    go_hotel_only()
    end_app()


def go_hotel_only():
    result = search_hotel_only('HRG', '010121', '100121', '7', '7', 'LABRANDA Royal Makadi')
    print(result)
    if result:
        scan_for_data()


def start_up():
    # Countdown timer
    print("Starting", end="")
    for i in range(0, 3):
        print(".", end=".")
        sleep(1)


def end_app():
    exit(0)
    print("Go")


if __name__ == '__main__':
    main()

