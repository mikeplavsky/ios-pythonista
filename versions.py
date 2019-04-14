import jira
jira.set_credentials()

from dialogs import list_dialog
import clipboard
import webbrowser
import ui

versions = dict()
epics = dict()

def create_page(name, data,source = ui.ListDataSource):

    page = ui.TableView()

    page.name = name
    page.data_source = source(data) 

    return page

@ui.in_background
def epic_issues(src, project, version, epic):

    title = src.title
    src.title = "..."

    issues = jira.get_epic_issues(
        project,
        version,
        epic)

    all = jira.fmt_issues(issues)

    all.insert(0,
        jira.get_features_header(issues))

    all.insert(
        0,
        f"{project}, {version}, {epic}")

    res = '\n\n'.join(all)

    src.title = title

    clipboard.set(res)
    webbrowser.open_new(
        'shortcuts://run-shortcut?name=CreateANote')

class Epics(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]

        create_button(
            cell, 
            "issues", 
            0.85, 
            lambda src: epic_issues(
                src,
                tableview.project,
                tableview.version,
                tableview.data_source.items[row]))

        return cell

@ui.in_background
def epics_page(src, project,version):

    title = src.title
    src.title = "..."

    key = (project,version)

    if not epics.get(key):
        epics[key] = jira.get_epics(*key)

    page = create_page(
        "Epics", 
        epics[key], 
        Epics)

    page.project = key[0]
    page.version = key[1]

    src.title = title
    nav.push_view(page)

def create_button(cell, title, left, action):

    btn = ui.Button(title=title)
    btn.center = (cell.content_view.width * left, cell.content_view.height * 0.5)
    btn.flex = 'LRTB'
    btn.action = action

    cell.content_view.add_subview(btn)

class Versions(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]

        create_button(
            cell, 
            "issues", 
            0.7, 
            None)

        create_button(
            cell, 
            "epics", 
            0.9, 
            lambda src: epics_page(
                src,
                tableview.project, 
                versions[tableview.project][row]))

        return cell

class Releases(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]

        create_button(
            cell, 
            "releases", 
            0.85, 
            lambda src: releases_page(
                src, 
                tableview.data_source.items[row]))

        return cell

@ui.in_background
def releases_page(src, proj):

    title = src.title    
    src.title = "..."

    if not versions.get(proj): 

        versions[proj] = jira.get_versions_names(
            dict(project=proj))

    page = create_page(
        "Releases", 
        versions[proj],
        Versions) 
    
    page.allows_selection = False
    page.project = proj

    src.title = title
    nav.push_view(page)

projects_page = create_page(
        "Products",[
        'RMADFE',
        'RMAZ',
        'QMMP'],
        Releases)

nav = ui.NavigationView(projects_page)
nav.present()
