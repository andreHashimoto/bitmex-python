from Bitmex import Bitmex
import sys

exchange = Bitmex(sys.argv[1], sys.argv[2])
print(exchange.order('XBTUSD', 'Buy', 1, 10000, 'Limit').json())