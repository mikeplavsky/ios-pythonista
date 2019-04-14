import jira
jira.set_credentials()

from dialogs import list_dialog
import clipboard
import webbrowser
import ui

versions = dict()
epics = dict()

def create_page(name, data, delegate):

    page = ui.TableView()

    page.name = name
    page.delegate = delegate
    page.data_source = ui.ListDataSource(data) 

    return page

class IssuesDelegate(object):
    def tableview_did_select(self, tv, section, row):

        epic = tv.data_source.items[row]

        issues = jira.get_epic_issues(tv.project,tv.version,epic)
        all = jira.fmt_issues(issues)

        all.insert(0,
            jira.get_features_header(issues))

        all.insert(
            0,
            f"{tv.project}, {tv.version}, {epic}")

        res = '\n\n'.join(all)

        clipboard.set(res)
        webbrowser.open_new(
            'shortcuts://run-shortcut?name=CreateANote')

class EpicsDelegate(object):
    def tableview_did_select(self, tv, section, row):

        version = tv.data_source.items[row]
        key = (tv.project,version)

        if not epics.get(key):
            epics[key] = jira.get_epics(*key)

        page = create_page(
            "Epics", 
            epics[key], 
            IssuesDelegate())

        page.project = key[0]
        page.version = key[1]

        nav.push_view(page)

class VersionsDelegate(object):

    def tableview_did_select(self, tv, section, row):

        proj = tv.data_source.items[row]
        if not versions.get(proj): 

            versions[proj] = jira.get_versions_names(
                dict(project=proj))

        page = create_page(
            "Releases", 
            versions[proj],
            EpicsDelegate()) 

        page.project = proj
        nav.push_view(page)

projects_page = create_page(
        "Products",[
        'RMADFE',
        'RMAZ',
        'QMMP'],
        VersionsDelegate())

nav = ui.NavigationView(projects_page)
nav.present()