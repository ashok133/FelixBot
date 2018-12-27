# firebaseconnector


'''
Sample data instances

engineInstance = {
    "timestamp": str(datetime.datetime.utcnow()),
    "engineID": 1134,
    "lat": 39.169491,
    "lng": -86.533597,
    "fuelAirRatio": 14.5, #14.5:1 is average
    "volumetricEfficiency": 90, #percentage
    "thermalEfficiency": 80, #percentage
    "peakPressure": 1380, #psi
    "oilStatus": "ok", #ok/warn/fatal
    "batteryStatus": 69, #percent
    "distanceDriven": 6888, #miles
    "fuelConsumed": 272, # ~gallons, distance/26
    "currentSpeed": 60 #miles per hr
}

faultLogInstance = {
    "timestamp": "2018-12-04 00:44:49.468157",
    "engineID": 1134,
    "lat": 39.169491,
    "lng": -86.533597,
    "fuelAirRatio": 14.5, #14.5:1 is average
    "volumetricEfficiency": 90, #percentage
    "thermalEfficiency": 80, #percentage
    "peakPressure": 1380, #psi
    "oilStatus": "ok", #ok/warn/fatal
    "batteryStatus": 69, #percent
    "distanceDriven": 6888, #miles
    "fuelConsumed": 272, # ~gallons, distance/26
    "currentSpeed": 60 #miles per hr
}
'''

import pyrebase
import datetime

def push(data, child):
    db.child(child).push(data)

def readAll(child):
    return db.child(child).get()

def readLast(child):
    allLogs =  db.child(child).get().val()
    return allLogs[str(next(reversed(allLogs)))]

def fetchVitalStats():
    return readLast('faultLog')

config = {
  "apiKey": "AIzaSyBAfbolzf2jdauPwuSUxQ9pkPe0HbinYb8",
  "authDomain": "cumminsinc-224004.firebaseapp.com",
  "databaseURL": "https://cumminsinc-224004.firebaseio.com",
  "storageBucket": "cumminsinc-224004.appspot.com",
  "serviceAccount": "credentials/serviceCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# print (fetchVitalStats())
