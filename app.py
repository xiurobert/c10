#!/bin/env/python

from flask import Flask, render_template
import json
import requests

rafael = Flask(__name__)


@rafael.route("/")
def index():

    returnedjson = requests.get("https://launchlibrary.net/1.4/launch/next/5").json()
    print(returnedjson)
    return render_template("index.html", launches=returnedjson["launches"])