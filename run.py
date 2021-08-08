from flask import Flask, render_template
import requests , schedule, json
import pymonad.tools
from pymonad.tools import curry
from pymonad.reader import Compose

@curry(2)
def add(a, b):
    c = b
    total = a
    for i in range(len(total)) :
        b = total[i]
        c += b
          
    return c

app = Flask(__name__)

def indo():
    api_url = "https://api.kawalcorona.com/indonesia/"
    rstl = requests.get(api_url).json()
    return rstl

r_indo = schedule.every(2).seconds.do(indo)
data_indo = indo() 

@app.route("/")
def index() :
    return render_template("covid.html", data_indo=data_indo)

@app.route("/artikel")
def artikel() :
    return render_template("article.html")

@app.route("/provinsi")
def covidprovinsi() :
    positif = []
    sembuh = []
    meninggal = []
    covidprovinsi = requests.get("https://api.kawalcorona.com/indonesia/provinsi/")
    dataprovinsi = covidprovinsi.json()
    totaldataprov = dataprovinsi
    for i in range(len(dataprovinsi)) :
        a = int(f"{dataprovinsi[i]['attributes']['Kasus_Posi']}")
        positif.append(a)
    for i in range(len(dataprovinsi)) :
        a = int(f"{dataprovinsi[i]['attributes']['Kasus_Semb']}")
        sembuh.append(a)
    for i in range(len(dataprovinsi)) :
        a = int(f"{dataprovinsi[i]['attributes']['Kasus_Meni']}")
        meninggal.append(a)
    total_positif = add(positif, 0)
    total_meninggal = add(meninggal, 0)
    total_sembuh = add(sembuh, 0)
    return render_template('provinsi.html', totaldataprov = totaldataprov, len = len(totaldataprov), 
    total_positif = total_positif, total_meninggal = total_meninggal, 
    total_sembuh = total_sembuh)

@app.route("/rumahsakit")
def rumahsakit():
    rumahsakit = requests.get("https://dekontaminasi.com/api/id/covid19/hospitals")
    datars = rumahsakit.json()
    totaldatars = datars
    return render_template('rumahsakit.html', totaldatars = totaldatars, len = len(totaldatars))

r_provinsi = schedule.every(2).seconds.do(covidprovinsi)

if __name__ == "__main__" :
    app.run(debug=True)