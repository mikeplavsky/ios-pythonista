import jira
jira.set_credentials()

from dialogs import list_dialog
import clipboard
import webbrowser

project = list_dialog(
    items=[
        'RMADFE',
        'RMAZ',
        'QMMP'])
        
vs = jira.get_versions_names(
    dict(project= project))

version = list_dialog(items=vs)
epics = jira.get_epics(project, version)

while True:

    epic = list_dialog(items=epics)
    if not epic:
        break

    issues = jira.get_epic_issues(project,version,epic)
    all = jira.fmt_issues(issues)

    all.insert(
        0,
        f"{project}, {version}, {epic}")
    res = '\n\n'.join(all)

    clipboard.set(res)
    webbrowser.open_new(
        'shortcuts://run-shortcut?name=CreateANote')

