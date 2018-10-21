#!/bin/env/python

from flask import Flask, render_template
import json
import requests

from pandas import DataFrame, read_csv
from plotly.offline import plot
import plotly.graph_objs as go

rafael = Flask(__name__)


@rafael.route("/")
def index():

    returnedjson = requests.get("https://launchlibrary.net/1.4/launch/next/5").json()

    # Iterate through launch pad location and collect weather
    apikey = "668e54896308f11a684be9ecf1020f6e"
    paddata = []
    for launch in returnedjson["launches"]:
        paddict = dict()
        paddict["lat"] = launch["location"]["pads"][0]["latitude"]
        paddict["lon"] = launch["location"]["pads"][0]["longitude"]

        openweathermap = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={paddict['lat']}&lon={paddict['lon']}&appid={apikey}").json()

        paddict["weather_general"] = openweathermap["weather"][0]["main"]
        paddict["temp"] = str(round(int(openweathermap["main"]["temp"]) - 273.15, 2))
        paddict["humidity"] = openweathermap["main"]["humidity"]
        #paddict["visibility"] = openweathermap["visibility"]
        paddict["windspeed"] = openweathermap["wind"]["speed"]
        #paddict["winddirection"] = openweathermap["wind"]["deg"]
        paddict["cloudpercent"] = openweathermap["clouds"]["all"]
        #paddict["rainvol"] = openweathermap["rain"]["3h"]
        #paddict["snowvol"] = openweathermap["snow"]["3h"]

        paddata.append(paddict)

    #print(paddata)
    return render_template("index.html", launches=returnedjson["launches"], padinfo=paddata)


@rafael.route("/spacex")
def spacex():

    returnjson = requests.get("https://api.spacexdata.com/v3/launches").json()
    return render_template("spacex_rocketlaunch.html", launches=returnjson)


@rafael.route("/graphviz/spacex")
def spacex_viz():
    # Plot Code

    # Generate DF and cut off other columns
    dataDF = read_csv("static/spacex_launch_data.csv")[["Date", "Payload Mass (kg)"]].copy()
    data = [
        go.Scatter(
            x=dataDF["Date"],
            y=dataDF["Payload Mass (kg)"]
        )
    ]
    layout = dict(title = 'Payload Mass/KG vs Launch Date',
                  xaxis = dict(title="Launch Date"),
                  yaxis = dict(title = "Payload Mass (KG)"))

    results = plot(dict(data=data, layout=layout), output_type="div")

    return render_template("spacex_graphviz.html", graph0=results)


