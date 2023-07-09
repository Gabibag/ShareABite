import sqlite3

import requests
from flask import Flask, render_template, request, jsonify, json
import googlemaps

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/getFoodTypes', methods=['get'])
def getFoodTypes():
    # get food types from database
    return [org['food'] for org in
            sqlite3.connect('database.db').cursor().execute("SELECT * FROM organizations").fetchall()]


@app.route('/api/getClosestOrganization', methods=['post'])
def getDatabase():
    print("req" + str(request.json))
    food = request.json['food'].lower()
    local = request.json['location'].lower()
    if food == "":
        print("no food type specified")
        return jsonify({'msg': 'no food type specified'}
                       ), 400
    if local == "":
        print("no location specified")
        return jsonify({'msg': 'no location specified'}
                       ), 400

    # get organization from database
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    organizations = cur.execute("SELECT * FROM main.organizations").fetchall()
    conn.close()
    orgs = []
    print(organizations)
    for org in organizations:
        if org[2] == food or org[2] == "":
            orgs.append(org)

    if len(orgs) == 0:
        return

    orgsdist = []
    for org in orgs:
        get = getClosestOrg(local, org[1]).get('duration').get('text')
        print(get)
        orgsdist.append({org[0], get})
    # sort orgdist by distance, the smaller the distance, the closer it is. orgsdist[0] is the distance each org is
    # from you

    print(orgsdist)

    print(orgsdist[0])
    st = ""
    nums = ["1,", "2,", "3,", "4,", "5,", "6,", "7,", "8,", "9,", "0,"]
    for org in orgsdist:
        str1 = list(org)[0]
        str2 = list(org)[1]
        if any(str in nums for str2 in nums):
            st += str(list(org)[0] + " is " + list(org)[1] + " from you") + "\n"
        else:
            st += str(list(org)[1] + " is " + list(org)[0] + " from you") + "\n"

    print(st)
    return st


@app.post('/api/imageRec')
def imageRec():
    file = request.files['file']
    # file should be an image

    # return format:
    # return jsonify({'msg': '{content of image}'})
    return


def getClosestOrg(loc1, loc2):
    api_key = 'AIzaSyB6XaktjH_OGhA2EbGHAYydW61Qqnv3Hkk'
    source = loc1
    dest = loc2
    gmaps = googlemaps.Client(key='AIzaSyB6XaktjH_OGhA2EbGHAYydW61Qqnv3Hkk')

    # Requires cities name
    my_dist = gmaps.distance_matrix(loc1, loc2)['rows'][0]['elements'][0]

    # Printing the result
    print(my_dist)
    # url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    # x = requests.get(url + 'origins = ' + source +
    #                  '&destinations = ' + dest +
    #                  '&key = ' + api_key).json()
    # print(x)

    return my_dist


if __name__ == '__main__':
    app.run()
