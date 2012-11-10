from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from locaobjects import *
import json

SODA = building((37.875238,-122.258911), (37.875766,-122.258417), [], "Soda Hall")
HOME = building((37.878628,-122.261212), (37.878871,-122.261), [], "Home")
QUALCOMM = building((37.874487,-122.258953), (37.87487,-122.258715), [], "Qualcomm Cyber Cafe")
DOE = building((37.871758,-122.259769), (37.872609,-122.259195), [], "Doe Memorial Library")


buildings = [HOME, SODA, QUALCOMM, DOE]
#sched = schedule({0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None})
paths = []
NULL = -1
START = 0
PATH = 1
START_TIME = 0
state = NULL
ATTEND_THRES = 9000

reqs = [{"latitude": 37.878749, "longitude": -122.26109, "timestamp":0}, {"latitude":37.877513, "longitude": -122.260634, "timestamp":1}, {"latitude":37.875125, "longitude": -122.260135, "timestamp":2}, {"latitude":37.87529, "longitude": -122.258606, "timestamp":3}, {"latitude": 37.87486, "longitude": -122.257941, "timestamp":4}, {"latitude": 37.873865, "longitude": -122.257656, "timestamp":5}, {"latitude": 37.873901, "longitude": -122.258598, "timestamp":6}, {"latitude": 37.874633, "longitude": -122.258893, "timestamp":7}]

def report_coordinates(request):
  "Expects coordinates and a timestamp in the POST. Save this to the user's model."
  "POST is a dictionary with parameters: latitude, longitude, timestamp (epoch time)"
  reqs.append(request)

def whereIam(location):
  for building in buildings:
    if building.contains(location):
      return building
  return None

def v3_epoly(request):
  return render_to_response("v3_epoly.js")

def presentation(request):
  return render_to_response("cartime.html")

def presentation_data(request):
  """Returns a JSON containing all the data for the final presentation. JSON should be an array of paths, each containing the building the path starts at. Eg:
  [{
     'start':{
       'building_name':<building_name>,
       'coordinates':<coordinates>,
       'start_time':<int>,
       'end_time':<int>,
       'total_time_spent': <int>
       'comp_activity':{
         'facebook':20 <mins>,
         '9gag': 10000 <mins>,
         'youcorn': 60 <mins>,
         'msword': 0.1 <mins>
       }
       'lectures':[
         {
           'lecture_name':<lecture_name>,
           'lecture_time':<lecture_location>,
           'attended':<True/False>
         },...
       ]
     },
     'path':{
       'start_time':<int>,
       'end_time':<int>,
       'total_time_spent': <int>
       'lectures':[
         {
           'lecture_name':<lecture_name>,
           'lecture_time':<lecture_location>,
           'attended':<True/False>
         },
       ]
       'locations':[
       ]
     }
   },...
  ]
  """
  global state,buildings,paths,ATTEND_THRES,START_TIME, sched
  for req in reqs:
    location = tuple([req["latitude"], req["longitude"]])
    time = req["timestamp"]
    building = whereIam(location)
    location = str(req["latitude"]) + "," + str(req["longitude"])
    if(state == NULL):
      json_dict = {"start":{}, "path":{}}
      START_TIME = time
      if(building):
        state = START
        json_dict["start"]["start_time"] = START_TIME
        json_dict["start"]["building_name"] = building.name()
        json_dict["start"]["coordinates"] = location
        json_dict["start"]["lectures"] = building.gen_lect_dict()
      else:
        state = PATH
        json_dict["path"]["start_time"] = START_TIME
        json_dict["path"]["locations"] = [location]
      paths.append(json_dict)
    elif(state == START):
      json_dict = paths[-1]
      json_dict["start"]["end_time"] = time
      json_dict["start"]["total_time_spent"] = time - START_TIME
      if(START_TIME - time >= ATTEND_THRES):
        for lecture in json_dict["start"]["lectures"]:
          lecture["attend"] = False
      if(not building):
        START_TIME = time
        state = PATH
        json_dict["path"]["locations"] = []
        json_dict["path"]["start_time"] = START_TIME
    elif(state == PATH):
      pron_dict = paths[-1]
      json_dict["path"]["end_time"] = time
      json_dict["path"]["total_time_spent"] = time - START_TIME
      #json_dict["path"]["lectures"] += sched.lec_list(time)
      json_dict["path"]["locations"].append(location) 
      if(building):
        state = START
        json_dict = {"start":{}, "path":{}}
        START_TIME = time
        state = START
        json_dict["start"]["start_time"] = START_TIME
        json_dict["start"]["building_name"] = building.name()
        json_dict["start"]["coordinates"] = location
        json_dict["start"]["lectures"] = building.gen_lect_dict()
        paths.append(json_dict)
  AT = ActivityTracker()
  AT.populate_comp_activity(paths)
  print paths
  return HttpResponse(json.dumps({"data":paths}))
