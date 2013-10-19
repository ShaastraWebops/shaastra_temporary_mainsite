from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('idiotPortal.views',
    # Examples:
    # url(r'^$', 'LibPortalTrial.views.home', name='home'),
    # url(r'^LibPortalTrial/', include('LibPortalTrial.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'register'),
    url(r'^register/$', 'register'),
    url(r'^registered/$', 'registered'),
    url(r'^login/$', 'userLogin'),
    url(r'^logout/$', 'userLogout'),
    url(r'^loggedOut/$', 'userLoggedOut'),
    url(r'^librarianPortal/(?P<user_id>\d+)/$', 'librarianPortal'),
    url(r'^addBook/(?P<user_id>\d+)/$', 'libPortalAddBook'),
    url(r'^editBook/(?P<user_id>\d+)/$', 'libPortalEditBook'),
    url(r'^deleteBook/(?P<user_id>\d+)/$', 'libPortalDeleteBook'),
    url(r'^userPortal/(?P<user_id>\d+)/$', 'userPortal'),
    url(r'^order/(?P<user_id>\d+)/$', 'userPortalOrderBook'),
    url(r'^returnBook/(?P<user_id>\d+)/$', 'userPortalReturnBook'),
)  
urlpatterns +=   patterns('',url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}))

