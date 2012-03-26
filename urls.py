from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SoundDrop.views.home', name='home'),
    # url(r'^SoundDrop/', include('SoundDrop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # show the index from /
    url(r'^$', 'sounds.views.main'),

    # Temporary serving of media when using built-in django server in Debug mode
    url(r'^recordings/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT+'recordings',
        }),
)
