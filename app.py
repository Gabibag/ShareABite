import sqlite3

import requests
from flask import Flask, render_template, request, jsonify, json, send_file
import googlemaps

app = Flask(__name__)
import os
import openai
import dotenv


@app.route('/')
def index():
    return render_template('/pages/homepage.html')

@app.route('/<path:url>', methods=['get'])
def sendPage(url):
    # check to see if the file exists, if not, return 404
    if not os.path.isfile("templates/pages/" + url + ".html"):
        return "404"
    return render_template('/pages/' + url + '.html')

@app.route('/api/getFoodTypes', methods=['get'])
def getFoodTypes():
    # get food types from database
    return [org['food'] for org in
            sqlite3.connect('database.db').cursor().execute("SELECT * FROM organizations").fetchall()]

@app.route("/image/<path:url>", methods=['get'])
def returnImage(url):
    print("aaaa")
    return send_file("static/Image/" + url, mimetype='image/gif')

@app.route("/script/<path:url>", methods=['get'])
def returnJs(url):
    return send_file("templates/scripts/" + url)
@app.route("/style/<path:url>", methods=['get'])
def returnCSS(url):
    return send_file("templates/styles/" + url)


@app.route('/api/getClosestOrganization', methods=['post'])
def getDatabase():
    food = request.json['food'].lower()
    local = request.json['location'].lower()
    print(food)
    print(local)
    organizations = sqlite3.connect('database.sqlite').cursor().execute("SELECT * FROM main.organizations").fetchall()
    orgs = []
    st = ""
    for org in organizations:
        if org[2] == food or org[2] == "":
            orgs.append(org)
            print(org)
            st += str(org[0]) + "\n"
    if len(orgs) == 0:
        return "No organizations found"
    
    try:
        orgsdist = []
        for org in orgs:
            get = getClosestOrg(local, org[1]).get('duration').get('text')
            print(get)
            orgsdist.append({org[0], get})
        
        nums = ["1,", "2,", "3,", "4,", "5,", "6,", "7,", "8,", "9,", "0,"]
        for org in orgsdist:
            str1 = list(org)[0]
            str2 = list(org)[1]
            if any(str in nums for str2 in nums):
                st += str(list(org)[0] + " is " + list(org)[1] + " from you") + "\n"
            else:
                st += str(list(org)[1] + " is " + list(org)[0] + " from you") + "\n"
    except:
        st += "\nTime unavailable"

    print(st)
    return st


@app.post('/api/imageRec')
def imageRec():
    file = request.files['file']
    dotenv.load_dotenv()
    openai.api_key = os.getenv('key')
    result = file.read()
    food = getFoodTypes()  # returns foods that organizations are asking for
    for x in result:
        food += x[1] + " "
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "In this sentence pick out the name of the every main food item: "
                        + str(food) + ". Only return the name of the food items and nothing else. for example 'beef stew', "
                        "'carrots', 'spinach'"}
        ]
    )
    return completion.choices[0].message.content.split(",")


def getClosestOrg(loc1, loc2):
    return googlemaps.Client(key='[redacted]').distance_matrix(loc1, loc2)['rows'][0]['elements'][0]


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
