import os

from django import http
from django.conf.urls import patterns, url
from django.template.context import RequestContext
from django.template import Template


USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.10 (maverick) Firefox/3.6.18'
BROWSCAP_FILE = os.path.join(os.path.dirname(__file__), 'data', 'browscap_14_05_2012.csv')
DOWNLOAD_URL = 'http://raw.github.com/CodeScaleInc/django-pybrowscap/develop/django_pybrowscap/tests/data/browscap_14_05_2012.csv'


urlpatterns = patterns('django_pybrowscap.tests',
                       url(r'^$', 'view', name='view'),
                       url(r'^robots.txt$', 'robots', name='robots')
                       )


def view(request):
    context = RequestContext(request, {'browser': getattr(request, 'browser', None)})
    return http.HttpResponse(Template(u'').render(context), mimetype='text/html')


def robots(request):
    context = RequestContext(request, {'browser': getattr(request, 'browser', None)})
    template = Template('User-agent: *\nDisallow:')
    return http.HttpResponse(template.render(context), mimetype='text/plain')


from .test_middleware import *
from .management.commands.test_download_browscap import *