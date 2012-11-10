from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import locaobjects
import json

HOME = building((2,3), (8,10), [], "Home")
SODA = building((7,7), (10,10), [], "Soda")
QUALCOMM = building((10,50), (70,80), [], "Qualcomm")
MAINSTACKS = building((1,1), (3,3), [], "Mainstacks")


buildings = [HOME, SODA, QUALCOMM, MAINSTACKS]
paths = []
NULL = -1
START = 0
PATH = 1
START_TIME = 0
state = NULL
ATTEND_THRES = 9000

req = {}

def report_coordinates(request):
  "Expects coordinates and a timestamp in the POST. Save this to the user's model."
  "POST is a dictionary with parameters: latitude, longitude, timestamp (epoch time)"
  req = request

def whereIam(location):
  for building in buildings:
    if building.contains(location):
      return building
  return None


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
  location = str(req["longitude"]) + "," + str(req["latitude"])
  time = req["timestamp"]
  building = whereIam(location)
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
      json_dict["path"]["lectures"] = schedule.lecture_list(time)
      json_dict["path"]["locations"] = [location]
    paths.append(json_dict)
  elif(state == START):
    json_dict = paths[-1]
    json_dict["start"]["end_time"] = time
    json_dict["start"]["total_time_spent"] = START_TIME - time
    if(START_TIME - time >= ATTEND_THRES):
      for lecture in json_dict["start"]["lectures"]:
        lecture["attend"] = False
    if(not building):
      START_TIME = time
      state = PATH
  elif(state == PATH):
    json_dict = paths[-1]
    json_dict["path"]["end_time"] = time
    json_dict["path"]["total_time_spent"] = START_TIME - time
    json_dict["path"]["lectures"] += schedule.lecture_list(time)
    json_dict["path"]["locations"] += [location] 
    if(building):
      state = NULL
  AT = ActivityTracker()
  AT.populate_comp_activity(paths)
  return HttpResponse(json.dumps({"data":paths}))
