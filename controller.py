import decimal
import os
from time import sleep
import pyautogui
import numpy as nm
import cv2
from PIL import ImageGrab
import pytesseract
from models import StaticVariables, ComparisonRecord, ComparisonResult


pyautogui.FAILSAFE = True


def no_offers():
    result = False
    if get_starting_position('message.png'):
        pyautogui.press('escape')
        result = True
    return result


def search_hotel_only(row_record):
    """ Apply Bistro parameters inputs """

    result = False
    click_location('reset_entry.png', 2, 10)
    click_location('customer_1.png')
    click_location('hotel_only.png', 2, 10)
    click_location('dest_3lc.png', 110, 10)
    insert_text(row_record.destination)
    click_location('arrival_date.png', 130, 10)
    insert_text(row_record.arrival)
    insert_text(row_record.departure)
    insert_text(str(row_record.duration_from))
    send_tabs(1)
    insert_text(str(row_record.duration_till))
    click_location('hotel_name.png', 100, 10)
    insert_text(row_record.hotel_name)

    click_location('board_selector.png', 2, 10)
    select_board(row_record.board)

    click_location('btn_update.png', 2, 10)
    if not no_offers():
        result = find_region()
        if result:
            result = find_hotel()
        if result:
            result = find_first_result()

    return result


def select_board(board):
    if board == '':
        click_location('board_selector.png', 2, 10)
    else:
        number_of_downs = 0
        if board == 'RO':
            number_of_downs = 1
        elif board == 'BB':
            number_of_downs = 2
        elif board == 'HB':
            number_of_downs = 3
        elif board == 'FB':
            number_of_downs = 4
        elif board == 'AI':
            number_of_downs = 5

        for i in range(1, number_of_downs):
            pyautogui.press('down')
        pyautogui.press('enter')


def find_region():
    """ To check if search result shows region & selects the first region """

    region = wait_for_update('update_done_1A.png', 'update_done_1B.png')
    result = region[0]
    if result:
        click_location(region[1], 15, 30)
    return result


def find_hotel():
    """ To check if search result shows hotel & selects the first hotel """

    hotel = wait_for_update('update_done_2A.png', 'update_done_2B.png')
    result = hotel[0]
    if result:
        click_location(hotel[1], 10, 50)
    return result


def find_first_result():
    """ select the first date result """
    result = False
    print('start selecting first result')
    if wait_for_update('data_found.png')[0]:
        result = True
    print(result)
    return result


def scan_for_data(row_record):
    click_location('data_found.png', 100, 10)
    first_search = True

    while row_record.fti_price is None or row_record.competitor_price is None:
        if first_search:
            first_search = False
        else:
            pyautogui.click()
            pyautogui.press('down')

        if get_starting_position('skip_selection.png'):
            pyautogui.press('down')

        start_position = get_starting_position('start_selection.png')
        end_position = get_starting_position('end_selection.png')
        pyautogui.moveTo([start_position.left + 100, start_position.top + 10])

        if start_position and end_position:
            image_to_crop = [start_position.left + 43, start_position.top - 3, end_position.left, end_position.top + 15]
            # image_to_string(image_to_crop)
            comparison_result = ComparisonResult(image_to_string(image_to_crop))

            print(comparison_result)

            if comparison_result.operator == 'FTI' and row_record.fti_price is None:
                row_record.fti_price = get_price()
            if comparison_result.operator != 'FTI' and row_record.competitor_price is None:
                row_record.competitor_name = comparison_result.operator
                row_record.competitor_price = get_price()

            # If data reached the end
            if data_ended():
                break
        else:
            print('error')
    return row_record


def data_ended():
    result = get_starting_position('data_ended.png') is not None
    return result


def get_price():
    result = None
    pyautogui.doubleClick()
    for i in range(0, 15):
        if get_starting_position('valid_booking.png'):
            price_location = get_starting_position('price_label.png')
            if price_location:
                image_to_crop = [price_location.left + 120, price_location.top,
                                 price_location.left + 300, price_location.top + 25]
                result = image_to_string(image_to_crop)
                result = parse_number(result)
                break
        elif get_starting_position('rq_booking.png') or get_starting_position('na_booking.png'):
            break
        sleep(0.5)
    pyautogui.press('escape')
    return result


def parse_number(string_number):
    result = ''
    valid_chars = '0123456789'
    for i in string_number:
        if i in valid_chars:
            result += i
        elif i == ',':
            result += '.'
    result = decimal.Decimal(result) / 2
    result = round(result, 2)
    return result


def wait_for_update(img_name, second_img=None):
    result = [False, None]
    for x in range(0, 10):
        sleep(1)
        if get_starting_position(img_name) is not None:
            result = [True, img_name]
            break
        elif second_img is not None:
            if get_starting_position(second_img) is not None:
                result = [True, second_img]
                break
    return result


def insert_text(text_to_insert):
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.keyDown('backspace')
    pyautogui.keyUp('backspace')
    pyautogui.write(text_to_insert)


def click_location(img_name, move_left=0, move_down=0, double_click=False):
    customer_1_position = get_starting_position(img_name)
    if customer_1_position:
        pyautogui.moveTo(customer_1_position[0] + move_left, customer_1_position[1] + move_down)
        if double_click:
            pyautogui.click(customer_1_position[0] + move_left, customer_1_position[1] + move_down,
                            clicks=2, interval=0.2)
        else:
            pyautogui.click(customer_1_position[0] + move_left, customer_1_position[1] + move_down)
        sleep(0.5)


def send_tabs(number_of_tabs):
    for i in range(0, number_of_tabs):
        pyautogui.hotkey('tab')


def get_starting_position(img_name):
    script_dir = os.path.dirname(__file__)
    needle_path = os.path.join(script_dir,
                               'needles', img_name)
    image_pos = pyautogui.locateOnScreen(needle_path)
    return image_pos


def image_to_string(part_to_crop):
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Bbox used to capture a specific area.
    cap = ImageGrab.grab(bbox=(part_to_crop[0], part_to_crop[1], part_to_crop[2], part_to_crop[3]))
    script_dir = os.path.dirname(__file__)
    # path = os.path.join(script_dir, 'ocr.png')
    # cap.save(path)
    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
        lang='eng')
    # print(tesstr)
    return tesstr
