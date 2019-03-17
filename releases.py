import jira
jira.set_credentials()

from dialogs import list_dialog

project = list_dialog(
    items=[
        'RMADFE',
        'RMAZ',
        'QMMP'])
        
print('getting...')
            
vs = jira.get_versions_names(
    dict(project= project))
    
list_dialog(items=vs)
