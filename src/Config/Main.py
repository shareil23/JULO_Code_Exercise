from flask import Flask, jsonify
from .Types import *

app                                         = Flask(__name__, template_folder='../Templates', static_folder='../Static')
app.config['SECRET_KEY']                     = SECRET_KEY
app.config['CACHE_TYPE']                     = "redis"
app.config['CACHE_DEFAULT_TIMEOUT']          = 604800  # 1 week cache time duration in seconds
app.config['CACHE_REDIS_URL']                = "redis://julo_redis_mini_wallet_services:6379"
app.config['SQLALCHEMY_DATABASE_URI']        = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 404 handling
@app.errorhandler(404)
def page_not_found(e):
    data = {
        "Status": 404,
        "Message": 'Not Found.'
    }

    return jsonify(data), 404
