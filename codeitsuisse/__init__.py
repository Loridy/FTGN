from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.ticker_stream
import codeitsuisse.routes.calendar

import codeitsuisse.routes.cryptocollapz
import codeitsuisse.routes.magiccauldrons