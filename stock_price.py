#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import logging
import os
from urllib.parse import urlencode
from urllib import request

from flask import Flask, jsonify

__version__ = '0.9.0'

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


def get_request(url, values=None):
    headers = {"User-Agent": "Python urllib", "Content-Type": "application/json"}
    if values:
        data = urlencode(values)
        full_url = "{url}?{data}".format(url=url, data=data)
    else:
        full_url = url
    app.logger.debug("Full URL is: {full_url}".format(full_url=full_url))
    _request = request.Request(full_url, headers=headers)
    try:
        response = request.urlopen(_request)
        result = response.read()
        response.close()
        return result
    except Exception as error:
        app.logger.exception(error)


def lookup_stock(name):
    url = "http://download.finance.yahoo.com/d/quotes.csv"
    values = dict(s=name, f="nl1r")
    return get_request(url, values)


def convert_to_dict(name, response):
    output = next(csv.reader([response]))
    result = dict(
        symbol=name,
        name=output[0],
        price=output[1])
    return result


@app.route("/")
def index():
    return "/stock/&lt;name&gt;"


@app.route("/healthz")
def health():
    app.logger.debug("health check")
    return "ok"


@app.route("/stock/<name>")
def stock(name):
    response = lookup_stock(name)
    if response:
        app.logger.info("Response from external API is: {response}".format(response=response))
        result = convert_to_dict(name, response.decode())
        result["success"] = True
        return jsonify(result)
    else:
        return jsonify(success=False)


if __name__ == "__main__":
    formatter = logging.Formatter(
        "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.getLevelName(LOG_LEVEL))
    app.run(host="0.0.0.0", port=PORT)
