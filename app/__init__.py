# -*- coding: utf-8 -*-

import logging
from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

logging.basicConfig(filename=app.config['LOGS'], level=logging.INFO)

from app import routes
