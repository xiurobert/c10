#!/bin/env/python

from flask import Flask, render_template
import json
import requests

rafael = Flask(__name__)


@rafael.route("/")
def index():

    returnedjson = requests.get("https://launchlibrary.net/1.4/launch/next/5").json()
    return render_template("index.html", launches=returnedjson["launches"])


@rafael.route("/spacex")
def spacex():

    returnjson = requests.get("https://api.spacexdata.com/v3/launches").json()
    return render_template("spacex.html", launches=returnjson)