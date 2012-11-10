import time
class building:
    def __init__(self, botleft, topright, lectures):
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
        d = {}
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
        
