from models import *
from converters import *

search_input = 'FT| PAUS Mon 06.07.20 © 7 HRG  Doppelzimmer Superior Low Cost Al'

#search_input = parse_row(search_input)

#print(search_input)

row_input = ComparisonResult(search_input)
print(row_input)
row_input.rate = 20
#row_input.set_rate(21)
print(row_input.operator[0])
print(row_input)