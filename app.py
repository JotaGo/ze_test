from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

import os
import math


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/areas'

mongo = PyMongo(app)

def distance(x1,y1,location):  
    R = 6373.0

    lat1 = math.radians(x1)
    lon1 = math.radians(y1)
    lat2 = math.radians(location[0])
    lon2 = math.radians(location[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


@app.route('/areas')
def areas():
    myAreas = mongo.db.areas.find()
    resp = dumps(myAreas)

    return resp

@app.route('/areas/<ide>', methods=['GET'])
def area(ide):
    myArea = mongo.db.areas.find_one({"pdvs.id":ide},{"pdvs":{"$elemMatch":{"id":ide}}})
    if myArea != None:
        resp = dumps(myArea)
        return resp
    else:
        return not_found()
    
@app.route('/new_partner', methods=['POST'])
def add_partner():
    _json = request.json
    _id = _json["pdvs"][0]["id"] 
    _tradingName = _json["pdvs"][0]["tradingName"]
    _ownerName = _json["pdvs"][0]["ownerName"] 
    _document = _json["pdvs"][0]["document"]
    _coverageArea_type= _json["pdvs"][0]["coverageArea"]["type"]
    _coverageArea_coordinates= _json["pdvs"][0]["coverageArea"]["coordinates"]        
    _address_type= _json["pdvs"][0]["address"]["type"]
    _address_coordinates= _json["pdvs"][0]["address"]["coordinates"] 
    
    myArea = mongo.db.areas.find()
    listAreas = list(myArea)
    _alreadyDocuments = [partners['document'] for item in listAreas for partners in item['pdvs']]
    _alreadyID = [partners['id'] for item in listAreas for partners in item['pdvs']]    

    if _coverageArea_type == 'MultiPolygon' and _address_type == 'Point' and _document not in _alreadyDocuments and _id not in _alreadyID:

        update = mongo.db.areas.update_one({},
            {
            "$push":{
                "pdvs":{
                        "id" : _id,
                        "tradingName" : _tradingName,
                        "ownerName" : _ownerName,
                        "document" : _document,
                        "coverageArea":{
                            "type" : _coverageArea_type,
                            "coordinates" : _coverageArea_coordinates
                            },
                        "address":{
                            "type" : _address_type,
                            "coordinates" : _address_coordinates
                            }
                        }
                    }
            }
        )
        resp = jsonify("Partner added succesfully")

        resp.status_code = 200
        return resp

    else:
        return not_found()


@app.route('/nearest_location/<location>')
def nearest_location(location):
    lat, lon = location.split('+')
    lat = float(lat)
    lon = float(lon)
    #print('lat:{}-lon:{}'.format(lat, lon))
    myArea = mongo.db.areas.find()
    listAreas = list(myArea)

    _coverageAreas = {partners["id"]:partners["coverageArea"]["coordinates"][0] for item in listAreas for partners in item['pdvs']}
    _address = {partners["id"]:partners["address"]["coordinates"] for item in listAreas for partners in item['pdvs']}

    minDistanceAddressAddressID = ""
    minDistanceAddress = 500.000
    for k, v in _address.items():
        calculatedDistanceAddress = distance(lat, lon, v)
        if calculatedDistanceAddress < minDistanceAddress:
            minDistanceAddressAddressID = k
            minDistanceAddress = calculatedDistanceAddress
            
    dicPolygonDistance = {}
    for k, v in _coverageAreas.items():
        for polygon in v:
            minDistanceCoverageArea = 500.000
            for coordinates in polygon:
                calculatedDistancePolygon = distance(lat, lon, coordinates)
                if calculatedDistancePolygon < minDistanceCoverageArea:
                    minDistanceCoverageArea = calculatedDistancePolygon
            dicPolygonDistance.update({k:minDistanceCoverageArea})

    minCoverageArea = min(dicPolygonDistance.keys(), key=(lambda k: dicPolygonDistance[k]))
    
    if dicPolygonDistance[minCoverageArea] < minDistanceAddress:
        nearestPartner = mongo.db.areas.find_one({},{"pdvs":{"$elemMatch":{"id":minCoverageArea}}})
        resp = dumps(nearestPartner)
        return resp
    elif dicPolygonDistance[minCoverageArea] > minDistanceAddress:
        nearestPartner = mongo.db.areas.find_one({},{"pdvs":{"$elemMatch":{"id":minDistanceAddressAddressID}}})
        resp = dumps(nearestPartner)
        return resp
    else:
        message = {
            'message' : "Out of range"
        }
        resp = jsonify(message)
        return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)