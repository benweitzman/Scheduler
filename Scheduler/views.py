from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login
from django.utils import simplejson
from Event.models import *
import itertools

from django import forms
from django.forms import ModelForm

class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.exclude(classes=None))

def getCourses(request,deptID):
    department = Department.objects.filter(id=deptID)[0]
    courses = list(department.classes.all().values("courseNumber","name").distinct())
    for course in courses:
        course['id'] = ClassObject.objects.filter(courseNumber=course['courseNumber'])[0].id
    print courses
    return HttpResponse(simplejson.dumps(courses))

def courseList(request):
    courses = dict()
    for i in range(0,100):
        print "course"+str(i)
        try:
            courseName = request.POST["course"+str(i)]
            coursenumber, coursename = courseName.split(" - ")
            print coursenumber, coursename
            courses[courseName] = ClassObject.objects.filter(courseNumber__startswith=coursenumber,name__startswith=coursename)
        except:
            break

    def timeToSlot(timeString):
        #print timeString
        if "NONE" in timeString or timeString == "":
            return 0
        try:
            #print timeString[2:4]
            am = "AM" in timeString
            hour = int(timeString[0:2])
            minutes = int(timeString[2:4])
            if am:
                return (hour-8)*12+(minutes/5)
            elif hour == 12:
                return minutes/5+48
            else:
                return hour*12+minutes/5+48
        except:
            return 0

    print courses
    needArrangements = list(itertools.product(*courses.values()))
    minConflict = 10000000
    minArragnement = None
    for arrangement in needArrangements:
        print arrangement
        table = [[0 for col in range(0,5)] for row in range(0,169)]
        for classobj in arrangement:
            days = classobj.days
            times = classobj.times
            if "~" in days:
                days = days.split("~")
                times = times.split("~")
                for index in len(days):
                    for char in days[index]:
                        startTime = timeToSlot(times[index][:5])
                        endTime = timeToSlot(times[index][7:])
                        cola = 0
                        if "T" in char:
                            cola = 1
                        elif "W" in char:
                            cola = 2
                        elif "R" in char:
                            cola = 3
                        elif "F" in char:
                            cola = 4
                        for i in range(startTime,endTime):
                            if table[i][cola] == 0:
                                table[i][cola] = 1
                            else:
                                table[i][cola] = 100

            elif "NONE" not in days:
                print days
                for char in days:
                    #print char
                    startTime = timeToSlot(times[:5])
                    endTime = timeToSlot(times[7:])
                    cola = 0
                    if "T" in char:
                        cola = 1
                    elif "W" in char:
                        cola = 2
                    elif "R" in char:
                        cola = 3
                    elif "F" in char:
                        cola = 4
                    print char, startTime, endTime
                    for i in range(startTime,endTime):
                        if table[i][cola] == 0:
                            table[i][cola] = 1
                        else:
                            table[i][cola] = 100
        tableSum = sum(sum(table[row][col] for row in range(0,169) ) for col in range(0,5))
        #print tableSum
        if tableSum < minConflict:
            minArragnement = arrangement
            minConflict = tableSum
    print minArragnement, minConflict
    calendarEvents = []
    for cls in minArragnement:
        day = cls.days
        times = cls.times.split("-")
        if not "NONE" in day:
            for char in day:
                date = 12
                if "T" in char:
                    date = 13
                if "W" in char:
                    date = 14
                if "R" in char:
                    date = 15
                if "F" in char:
                    date = 16
                startTime = times[0]
                endTime = times[1]
                startHour = int(startTime[0:2])
                if "P" in startTime:
                    startHour += 12
                startMinute = startTime[2:4]
                endHour = int(endTime[0:2])
                if "P" in endTime:
                    endHour += 12
                endMinute = endTime[2:4]
                calendarEvents.append({"day":date,"id":cls.id,"startHour":startHour,"startMinute":startMinute,"endHour":endHour,"endMinute":endMinute,"title":cls.name})
    return HttpResponse(simplejson.dumps(calendarEvents))

def index(request):
    c = RequestContext(request)
    user = request.user
    if user.is_authenticated():
        classes = ClassEvent.objects.filter(user=user)
        events = PersonalEvent.objects.filter(user=user)
    else:
        classes = None
        events = None

    departments = DepartmentForm()

    return render_to_response("index.html",RequestContext(request,{"classes":classes,
                                                                   "events":events,
                                                                   "departments":departments}))