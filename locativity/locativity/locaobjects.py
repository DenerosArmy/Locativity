import time
class building:
    def __init__(self, botleft, topright, lectures, name):
        self.botleft = botleft
        self.topright = topright
        self.name = name
        self.lectures = lectures # list
    def contains(self, position):
        x,y = self.position;
        return (botleft[0] <= x <= topright[0]) and (botleft[1] <= y <= topright[1])
    def name(self):
        return self.name;
    def lectures(self):
        return self.lectures
    def gen_lect_dict(self):
        d = []
        for lecture in self.lectures:
            d.append(lecture.get_dict())
        return d

class schedule:
    def __init__(self, dayToLectures):
        self.dayToLectures = dayToLectures
    def missed_lectures(self, time):
        lecture_list = []
        localtime = time.localtime()
        lectures = self.dayToLectures[localtime.tm_wday]
        for lecture in lectures:
            hstart, mstart = lecture.start()
            hend, mend = lecture.end()
            tmp = lecture.get_dict()
            if(60*hstart + mstart <= 60*localtime.tm_hour + localtime.tm_min):
                if(60*localtime.tm_hour + localtime.tm_min <= 60*hend + minend):
                    tmp["attended"] = True
                else:
                    tmp["attended"] = False
                lecture_list.append(tmp)
        return lecture_list
                        

class lecture:
    #timeEnd and timeStart are local times in the form (<weekday>, <hour>, <minute>)
    def __init__(self, name, timeStart, timeEnd, building):
        self.name = name
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.building = building
    def name(self):
        return name
    def start(self):
        return timeStart
    def end(self):
        return timeEnd
    def get_dict():
        return {"lecture_name": lecture.name(), "lecture_timeStart":lecture.timeStart(), "lecture_timeEnd":lecture.timeEnd(), "attended": True}
        
import urllib2, datetime

class ActivityTracker:
  
  the_key = ""

  def __init__(self):
    pass

  def get_url(self, key):
    return "https://www.rescuetime.com/anapi/data?key="+key

  def get_data(self, key, date=None):
    res = urllib2.urlopen(self.get_url(key))
    data = res.readlines()
    data.pop(0)
    if date == None:
      today = datetime.datetime.now()
      date = today.strftime("%Y-%m-%d")
      data = self.filter_raw_data(data, date)
    else:
      data = self.filter_raw_data(data, date)
    return data

  def filter_raw_data(self, data, date):
    num_entries = len(data)
    clean_data = []
    for i in range(num_entries):
      if data[i][0:10] == date:
        clean_data.append(self.process_entry(data[i]))
    return clean_data

  def process_entry(self, entry):
    cols = entry.split(",")
    new_ent = {}
    new_ent["activity"] = cols[3].lower().title().replace(".Com", ".com")
    new_ent["category"] = cols[4].lower().title()
    new_ent["productivity"] = cols[5].lower().title()
    new_ent["duration"] = cols[1][:-2]
    return new_ent

  def populate_comp_activity(self, presentation_data, date=None):
    """
    'comp_activity':[
      {
      'activity':'Facebook',
      'category':'Crap',
      'productivity':-99,
      'duration':25
      },...
    ]
    """
    data = self.get_data(ActivityTracker.the_key, date)
    curr = []
    curr_dur = 0
    for path in presentation_data:
      if len(data) > 0:
        cand_dur = curr_dur+int(data[0]["duration"])
      while len(data) > 0 and cand_dur < path["start"]["total_time_spent"]:
        curr.append(data.pop(0))
        curr_dur = cand_dur
        if len(data) > 0:
          cand_dur = curr_dur+int(data[0]["duration"])
      path["comp_activity"] = curr
      curr = []
