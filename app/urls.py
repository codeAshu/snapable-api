from django.conf.urls import patterns, include, url
from django.contrib import admin 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# other endpoints
import dashboard
import ajax
import hooks

# apis
import api.partner_v1
import api.private_v1

# custom error handlers
handler404 = lambda r: render(r, '404.txt', status=404, content_type='text/plain')
handler500 = lambda r: render(r, '500.txt', status=500, content_type='text/plain')

urlpatterns = patterns('',
    # redirect the root API to prevent error pages
    url(r'^$', lambda x: HttpResponseRedirect('http://snapable.com/')),
    # tell bots not to try and crawl the API
    url(r'^robots\.txt$', lambda r: render(r, 'robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', lambda r: render(r, 'humans.txt', content_type='text/plain')),

    # add admin
    (r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    (r'^control_tower/', include(dashboard.site.urls)),
    (r'^control_tower/ajax/', include(ajax.urls)),

    # handle webhooks
    (r'^hooks/', include(hooks.urls)),

    ## define all the API versions here ##
    # public APIs
    #url(r'', include(api.v1.SnapableApi().urls)),

    # partner APIs
    url(r'', include(api.partner_v1.SnapableApi().urls)),

    # private APIs
    url(r'', include(api.private_v1.SnapableApi().urls)),
)
