from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login
from Event.models import *

def index(request):
    c = RequestContext(request)
    user = request.user
    if user.is_authenticated():
        classes = ClassEvent.objects.filter(user=user)
        events = PersonalEvent.objects.filter(user=user)
    else:
        classes = None
        events = None

    departments = Department.objects.all()

    return render_to_response("index.html",RequestContext(request,{"classes":classes,
                                                                   "events":events}))