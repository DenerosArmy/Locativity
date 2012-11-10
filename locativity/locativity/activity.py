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
