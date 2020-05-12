import os
from time import sleep
import pyautogui
import numpy as nm
import cv2
from PIL import ImageGrab
import pytesseract

pyautogui.FAILSAFE = True


def search_hotel_only(destination, start_date, end_date, duration_from, duration_till, hotel_name):
    """ Apply Bistro parameters inputs """

    result = False
    click_location('customer_1.png')
    click_location('hotel_only.png', 2, 10)
    click_location('dest_3lc.png', 110, 10)
    insert_text(destination)
    click_location('arrival_date.png', 130, 10)
    insert_text(start_date)
    insert_text(end_date)
    insert_text(duration_from)
    send_tabs(1)
    insert_text(duration_till)
    click_location('hotel_name.png', 100, 10)
    insert_text(hotel_name)
    sleep(0.20)
    pyautogui.press('escape')
    click_location('btn_update.png', 2, 10)

    result = find_region()
    if result:
        result = find_hotel()
    if result:
        result = find_first_result()
    return result


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


def scan_for_data():
    click_location('data_found.png', 100, 10)
    first_search = True
    for i in range(0, 20):
        if first_search:
            first_search = False
        else:
            pyautogui.click()
            pyautogui.press('down')

        if get_starting_position('skip_selection.png'):
            pyautogui.press('down')

        start_position = get_starting_position('start_selection.png')
        end_position = get_starting_position('end_selection.png')
        if start_position and end_position:
            image_to_crop = [start_position.left, start_position.top - 3, end_position.left, end_position.top + 15]
            image_to_string(image_to_crop)
            get_price([start_position.left + 100, start_position.top + 10])
        else:
            print('error')


def get_price(location):
    result = None
    pyautogui.moveTo(location)
    pyautogui.doubleClick()
    for i in range(0, 15):
        if get_starting_position('valid_booking.png'):
            price_location = get_starting_position('price_label.png')
            if price_location:
                image_to_crop = [price_location.left + 120, price_location.top,
                                 price_location.left + 300, price_location.top + 25]
                image_to_string(image_to_crop)
                break
        elif get_starting_position('rq_booking.png') or get_starting_position('na_booking.png'):
            break
        sleep(0.5)
    pyautogui.press('escape')
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
    path = os.path.join(script_dir, 'ocr.png')
    # cap.save(path)
    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
        lang='eng')
    print(tesstr)
