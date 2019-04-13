import jira
jira.set_credentials()

from dialogs import list_dialog
import clipboard
import webbrowser
import ui

versions = dict()

class EpicsDelegate(object):
    def tableview_did_select(self, tv, section, row):
        pass

class VersionsDelegate(object):

    def tableview_did_select(self, tv, section, row):

        proj = tv.data_source.items[row]
        if not versions.get(proj): 

            versions[proj] = jira.get_versions_names(
                dict(project=proj))

        versions_page = ui.TableView()
        versions_page.data_source = ui.ListDataSource(versions[proj]) 

        nav.push_view(versions_page)

projects_page = ui.TableView()
projects_page.data_source = ui.ListDataSource( 
    items=[
        'RMADFE',
        'RMAZ',
        'QMMP'])

projects_page.delegate = VersionsDelegate()

nav = ui.NavigationView(projects_page)
nav.present()

exit()
        
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

