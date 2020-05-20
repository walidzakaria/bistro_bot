from time import strftime
from converters import parse_row


@staticmethod
class StaticVariables:
    current_record = 0
    last_record = 0


class ComparisonResult:

    def __init__(self, result_text):
        parsed_row = parse_row(result_text)
        self.operator = parsed_row[0]
        self.room_type = parsed_row[1]
        self.rate = 0

    def __str__(self):
        return f'operator: {self.operator}, room_type: {self.room_type}, rate: {self.rate}'

    def __dict__(self):
        return {
            "operator": self.operator,
            "room_type": self.room_type,
            "rate": self.rate
        }


class ComparisonRecord:

    def __init__(self, destination, arrival, departure, duration_from, duration_till, hotel_name, board, fti_price,
                 competitor_name, competitor_price):
        self.destination = destination
        self.arrival = arrival.strftime('%d%m%y')
        self.departure = departure.strftime('%d%m%y')
        self.duration_from = duration_from
        self.duration_till = duration_till
        self.hotel_name = hotel_name
        self.board = board
        self.fti_price = fti_price
        self.competitor_name = competitor_name
        self.competitor_price = competitor_price

    def __str__(self):
        return f'hotel: {self.hotel_name} ({self.arrival}-{self.departure})'

    def __dict__(self):
        return {
            "destination": self.destination,
            "arrival": self.arrival,
            "departure": self.departure,
            "duration_from": self.duration_from,
            "duration_till": self.duration_till,
            "hotel_name": self.hotel_name,
            "board": self.board,
            "fti_price": self.fti_price,
            "competitor_name": self.competitor_name,
            "competitor_price": self.competitor_price
        }
