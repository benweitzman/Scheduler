from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from Scheduler import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Scheduler.views.index'),
    url(r'^ajax/getcourses/(?P<deptID>\d*)$','Scheduler.views.getCourses'),
    url(r'^ajax/courses/$','Scheduler.views.courseList'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root':settings.STATIC_ROOT}),
    # url(r'^Scheduler/', include('Scheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
