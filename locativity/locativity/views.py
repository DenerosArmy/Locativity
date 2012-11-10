from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def report_coordinates(request):
  "Expects coordinates and a timestamp in the POST. Save this to the user's model."
  field = request.POST["field_name"]
  pass

def presentation_data(request):
  """Returns a JSON containing all the data for the final presentation. JSON should be an array of paths, each containing the building the path starts at. Eg:
  [{
     'start':{
       'building_name':<building_name>,
       'coordinates':<coordinates>,
       'total_time_spent':<duration>,
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
       'total_time_spent':<duration>,
       'lectures':[
         {
           'lecture_name':<lecture_name>,
           'lecture_time':<lecture_location>,
           'attended':<True/False>
         },...
       ]
     }
     'end':<coordinates>
   },...
  ]
  """
  return HttpResponse("json?")
