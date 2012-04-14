from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login
from django.utils import simplejson
from Event.models import *

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
    courses = list()
    for i in range(0,100):
        print "course"+str(i)
        try:
            courses.append(request.POST["course"+str(i)])
        except:
            break
    return HttpResponse(courses)

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