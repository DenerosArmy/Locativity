from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Web Services
    url(r'^$', 'locativity.views.home', name='home'),
    url(r'^showdata', 'locativity.views.presentation', name='presentation'),
    url(r'^v3_epoly.js', 'locativity.views.v3_epoly', name='v3_epoly'),

    # Endpoint Services
    # url(r'^$', 'locativity.views.home', name='home'),
    url(r'^report_coordinates', 'locativity.views.report_coordinates', name='report_coordinates'),
    url(r'^presentation_data', 'locativity.views.presentation_data', name='presentation_data'),

    # Examples:
    # url(r'^$', 'locativity.views.home', name='home'),
    # url(r'^locativity/', include('locativity.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
