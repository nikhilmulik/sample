from django.conf.urls import patterns, include, url
from django.conf import settings
from process_it.codes.main import AboutView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^about/', AboutView.as_view()),
	# Examples:
	# url(r'^$', 'Adroit.views.home', name='home'),
	# url(r'^Adroit/', include('Adroit.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),
	url(r'^process_it/', include('process_it.urls')),
	#url(r'^pre_alerts_processing/$', pre_alerts_processing),
	#url(r'^pre_alerts_master_sheet/$', pre_alerts_master_sheet),
	#url(r'^shipment_processing/$', shipment_processing),
	#url(r'^shipment_master_sheet/$', shipment_master_sheet),
	#url(r'^one_f_status_sheet/$', one_f_status_sheet),
	#url(r'^worldport_processing/$', worldport_processing),
	#url(r'^worldport_master_processing/$', worldport_master_processing),
	#url(r'^time/$', current_datetime),
	#(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_JS}),
	#(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_CSS}),
	#(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_IMG}),
	url(r'', include('process_it.urls')),
	url(r'^.*', include('process_it.urls')),
	
	
)
