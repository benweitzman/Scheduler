from django.core.management.base import BaseCommand, CommandError
import pycurl
from StringIO import StringIO
import urllib
import re
from string import strip
from Event.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        Department.objects.all().delete()
        ClassObject.objects.all().delete()
        c = pycurl.Curl()
        storage = StringIO()
        c.setopt(c.WRITEFUNCTION,storage.write)
        c.setopt(pycurl.URL,"https://webcenter.studentservices.tufts.edu/courses/main.asp")
        c.perform()
        c.close()
        terms = re.search(r"<select name=\"term\" size=\"1\">(.*?)</select>",storage.getvalue(),re.M|re.S)
        #print terms.group(0)
        term = re.search(r"value=\"([^\"\r\n]*)\"",terms.group(1)).group(1)
        print term
        departments = re.search(r"<select name=\"dept\" size=\"1\">(.*?)</select>",storage.getvalue(),re.M|re.S)
        deptIDs = re.findall(r"value = '([^'\r\n]*)'",departments.group(1))
        depts = re.findall(r">([^<\r\n]*)<",departments.group(1))
        depts.pop(0)
        for i in range(0, len(deptIDs)):
            departmentmodel = Department.objects.create(key=deptIDs[i], title=depts[i])
            departmentmodel.save()
        for department in deptIDs:
            c = pycurl.Curl()
            data = [
                ('term', term),
                ('dept', department),
                ('crse_time', "Courses+Offered+Any+Time"),
                ('submit', "Go")
            ]
            #print data
            post = urllib.urlencode(data)
            c.setopt(pycurl.POSTFIELDS, post)
            c.setopt(pycurl.URL, "https://webcenter.studentservices.tufts.edu/courses/subject_listing.asp")
            c.setopt(pycurl.POST, 1)
            c.setopt(c.WRITEFUNCTION, storage.write)
            c.perform()
            c.close()
            out = re.sub("<font[^>\r\n]*>", "", storage.getvalue())
            out = re.sub("<b>", "", out)
            out = re.sub("</b>", "", out)
            out = re.sub("<A[^>\r\n]*>", "", out)
            out = re.sub("<a[^>\r\n]*>", "", out)
            out = re.sub("</A>", "", out)
            out = re.sub("</a>", "", out)
            out = re.sub("<NOBR>", "", out)
            out = re.sub("</NOBR>", "", out)
            out = re.sub("<br>", "~", out)
            out = re.sub("<tr>", "", out)
            out = re.sub("</tr>", "", out)
            out = re.sub("<td[^>\r\n]*>", "<td ", out)
            out = re.sub("</td>", ">", out)
            out = re.sub("&nbsp;", "", out)
            matches = re.findall("<td([^>\r\n]*)>", out)
            #print matches
            deptObject = Department.objects.filter(key=department)[0]
            for key in range(0,len(matches)):
                if key >= 12 and key % 12 == 0:
                    if not re.findall("NOT REGISTER", matches[key + 3]) and not re.findall("NOT REGISTER", matches[key+11]):
                        closed = strip(matches[key])
                        callnum = strip(matches[key + 1])
                        course = strip(matches[key + 2])
                        title = strip(matches[key + 3])
                        days = strip(matches[key + 5])
                        if days == "":
                            days = "NONE"
                        times = strip(matches[key+6])
                        loc = strip(matches[key+7])
                        prof = strip(matches[key+10])
                        if times == "":
                            times = "NONE"
                        if "~" in loc:
                            days = days.split("~")
                            #print title, days

                            times = times.split("~")
                            loc = loc.split("~")
                            if len(loc) is 4 and loc[0] is not loc[1] and days[0] is days[1]:
                                days1 = days[0]+"~"+days[2]
                                times1 = times[0]+"~"+times[2]
                                loc1 = loc[0]
                                days2 = days[1]+"~"+days[3]
                                times2 = times[1]+"~"+times[3]
                                loc2 = loc[2]
                                classobj1 = ClassObject.objects.create(days=days1,times=times1,locations=loc1,
                                        closed=closed,courseNumber=course,callNumber=callnum,
                                        professor=prof,description="",name=title
                                        )
                                classobj1.save()
                                deptObject.classes.add(classobj1)
                                classobj2 = ClassObject.objects.create(days=days2,times=times2,locations=loc2,
                                    closed=closed,courseNumber=course,callNumber=callnum,
                                    professor=prof,description="",name=title
                                )
                                classobj2.save()
                                deptObject.classes.add(classobj2)
                                deptObject.save()
                                print deptObject
                            elif len(loc) is 2 and loc[0] is not loc[1] and days[0] is days[1]:
                                days1 = days[0]
                                times1 = times[0]
                                loc1 = loc[0]
                                days2 = days[1]
                                times2 = times[1]
                                loc2 = loc[1]
                                classobj1 = ClassObject.objects.create(days=days1,times=times1,locations=loc1,
                                    closed=closed,courseNumber=course,callNumber=callnum,
                                    professor=prof,description="",name=title
                                )
                                classobj1.save()
                                classobj2 = ClassObject.objects.create(days=days2,times=times2,locations=loc2,
                                    closed=closed,courseNumber=course,callNumber=callnum,
                                    professor=prof,description="",name=title
                                )
                                classobj2.save()
                                deptObject.classes.add(classobj1,classobj2).save()
                            elif len(loc) is 3:
                                pass
                            else:
                                classobj = ClassObject.objects.create(days=days[0]+"~"+days[1],
                                                                      times=times[0]+"~"+times[1],
                                                                      closed=closed,
                                        professor=prof,
                                locations=loc[0]+"~"+loc[1],
                                callNumber=callnum,
                                description="",
                                name=title,
                                courseNumber=course)
                                classobj.save()
                                deptObject.classes.add(classobj)
                                deptObject.save()
                                pass
                        else:
                            classobj = ClassObject.objects.create(days=days,
                                times=times,
                                closed=closed,
                                professor=prof,
                                locations=loc,
                                callNumber=callnum,
                                description="",
                                name=title,
                                courseNumber=course)
                            classobj.save()
                            deptObject.classes.add(classobj)
                            deptObject.save()
                            pass
