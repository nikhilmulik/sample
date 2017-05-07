from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^$', 'process_it.codes.main.index'),
	url(r'^validate/$', 'process_it.codes.main.validate'),
	url(r'^signOut/$', 'process_it.codes.main.signOut'),
        url(r'^aiLog/$', 'process_it.codes.main.aiLog'),


	url(r'^getMailBody/$', 'process_it.codes.datasource.getMailBody'),
	url(r'^getMailList/$', 'process_it.codes.datasource.getMailList'),
	url(r'^getTasks/$', 'process_it.codes.datasource.getTasks'),
	url(r'^mailAction/$', 'process_it.codes.datasource.mailAction'),
    url(r'^getDashboardCounts/$', 'process_it.codes.datasource.getDashboardCounts'),

	url(r'^bbPrealert/$', 'process_it.codes.prealert.bbPrealert'),
	url(r'^DFWbbPrealert/$', 'process_it.codes.prealert.DFWbbPrealert'),
	
	url(r'^temp0189/$', 'process_it.codes.prealert.temp0189'),
    url(r'^refreshScreen/$', 'process_it.codes.prealert.refreshScreen'),
    url(r'^showAll/$', 'process_it.codes.prealert.showAll'),

	url(r'^bbPrealertMaster/$', 'process_it.codes.prealertMaster.bbPrealertMaster'),
	url(r'^DFWbbPrealertMaster/$', 'process_it.codes.prealertMaster.DFWbbPrealertMaster'),


	url(r'^mawbAction/$', 'process_it.codes.mawbAction.mawbAction'),
	url(r'^addMawbEntry/$', 'process_it.codes.mawbAction.addMawbEntry'),
    url(r'^insertMawb/$', 'process_it.codes.mawbAction.insertMawb'),  # insert mawb from mails
	url(r'^chkHasMawb/$', 'process_it.codes.mawbAction.chkHasMawb'),
	url(r'^updateMawbEntry/$', 'process_it.codes.mawbAction.updateMawbEntry'),
    url(r'^rebookEntry/$', 'process_it.codes.mawbAction.rebookEntry'),
    url(r'^deleteMasters/$', 'process_it.codes.mawbAction.deleteMasters'),
    url(r'^moveMastersToPAP/$', 'process_it.codes.mawbAction.moveMastersToPAP'),
    url(r'^completeCOBToMasters/$', 'process_it.codes.mawbAction.completeCOBToMasters'),

    url(r'^validateMawbEntry/$', 'process_it.codes.views.validateMawbEntry'),
    url(r'^setClassCredentials/$', 'process_it.codes.views.setClassCredentials'),
    url(r'^airLinesDetails/$', 'process_it.codes.views.airLinesDetails'),

	url(r'^downloadAttachment.*$', 'process_it.codes.views.downloadAttachment'),
	url(r'^exportExcel/$', 'process_it.codes.views.exportExcel'),
	url(r'^preAlertExcel/$', 'process_it.codes.views.preAlertExcel'),
	url(r'^export_excel_new/$', 'process_it.codes.views.export_excel_new'),
	url(r'^DFWexportExcel/$', 'process_it.codes.views.DFWexportExcel'),
    url(r'^performEvalutation/$', 'process_it.codes.views.performEvalutation'),


	url(r'^moveInscope/$', 'process_it.codes.views.moveInscope'),
	url(r'^cobTracker/$', 'process_it.codes.views.cobTracker'),

    # url(r'^uploadBOSheet/$', 'process_it.codes.views.uploadBOSheet'),
    # url(r'^examplegrid/$', 'process_it.codes.views.grid_handler', name='grid_handler'),
    # url(r'^examplegrid/cfg/$', 'process_it.codes.views.grid_config', name='grid_config'),
    # url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    # url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),

    url(r'^displayLog/$','process_it.codes.views.displayLog'),
    url(r'^displayAllLog/$','process_it.codes.views.displayAllLog'),
    url(r'^mawbByDate/$', 'process_it.codes.views.mawbByDate'),
    url(r'^individualProcess/$','process_it.codes.views.individualProcess'),
    url(r'^extAiReport/$','process_it.codes.views.extAiReport'),
    
    
    url(r'^charts/$','process_it.codes.views.charts'),
 
)
