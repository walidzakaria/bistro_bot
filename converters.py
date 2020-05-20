
OPERATORS = [
    ('FT|', 'FTI'),
    ('FT', 'FTI'),
    ('SVF', '5vF'),
]

STANDARD_ROOMS = [
    ['FTI', ['Doppelzimmer', 'Doppelzimmer Landblick']]
]


def parse_operator(operator):
    result = operator
    for i in OPERATORS:
        if result == i[0]:
            result = i[1]
            break
    return result


def is_standard(operator, room_type):
    result = False
    for i in STANDARD_ROOMS:
        if i[0] == operator:
            if room_type in i[1]:
                result = True
                break
    return result


def parse_row(raw_data):
    result = raw_data.strip()

    result = result.strip().split()
    result = result[:-1]
    operator = result[0]
    operator = parse_operator(operator)
    room_type = " ".join(result[7:])
    result = operator, room_type
    return result

