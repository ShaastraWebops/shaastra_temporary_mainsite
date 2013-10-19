from django.conf.urls import patterns, include, url
import os.path
import settings
from mainsite_2014.settings import STATIC_URL
from django.views.generic.simple import redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
# For DajaxIce to work
from misc.dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forgot_password/(?P<password_key>.*)/$','users.views.forgot_password'),
    url(r'^forgot_password/success/$','users.views.forgot_password'),
    url(r'^user/register/activate/(?P<a_key>.*)/$','users.views.activate'),
    url(r'^/$', 'frontend.views.home'),#redirect_to, {'url': '/login/'}),
    url(r'^$', 'frontend.views.home'),#redirect_to, {'url': '/login/'}),
    url(r'^tdpsubmission$','users.views.submit_tdp'),
    url(r'^test/tdpsubmission$','users.views.submit_tdp'),
    url(r'^serenity$', 'frontend.views.serenity'),#redirect_to, {'url': '/login/'}),
    url(r'^files_upload$', 'files_upload.views.upload_file'),
    url(r'^dashboard$', 'frontend.views.dashboard'),
    url(r'^dashboard/$', 'frontend.views.dashboard'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
    url(dajaxice_config.dajaxice_url, include('misc.dajaxice.urls')), # For dajaxice to function corrently
)

urlpatterns += staticfiles_urlpatterns() # To enable serving static files
    
