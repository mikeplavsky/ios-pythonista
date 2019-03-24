import jira
jira.set_credentials()

from dialogs import list_dialog

project = list_dialog(
    items=[
        'RMADFE',
        'RMAZ',
        'QMMP'])
        
vs = jira.get_versions_names(
    dict(project= project))
version = list_dialog(items=vs)

epics = jira.get_epics(project, version)
list_dialog(items=epics)
