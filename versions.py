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

def change_title(f):
    def func(src, *args):

        title = src.title    
        src.title = "..."

        f(src,*args)

        src.title = title 

    return func

def create_note(all):

    res = '\n\n'.join(all)

    clipboard.set(res)
    webbrowser.open_new(
        'shortcuts://run-shortcut?name=CreateANote')

@ui.in_background
@change_title
def epic_issues(src, project, version, epic):

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

    create_note(all)

@ui.in_background
@change_title
def release_issues(src, project, version):

    issues = jira.get_release_issues(
        project,
        version) 

    all = jira.fmt_issues(issues)

    all.insert(0,
        jira.get_features_header(issues))

    all.insert(
        0,
        f"{project}, {version}")

    create_note(all)

def create_cell(ds,row, func = lambda x,r: x.items[r]):

    cell = ui.TableViewCell('subtitle')
    cell.text_label.text = func(ds,row)

    return cell

class Epics(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = create_cell(self, row)

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
@change_title
def epics_page(src, project,version):

    key = (project,version)

    if not epics.get(key):
        epics[key] = jira.get_epics(*key)

    page = create_page(
        "Epics", 
        epics[key], 
        Epics)

    page.project = key[0]
    page.version = key[1]

    nav.push_view(page)

def create_button(cell, title, left, action):

    btn = ui.Button(title=title)
    btn.center = (cell.content_view.width * left, cell.content_view.height * 0.5)
    btn.flex = 'LRTB'
    btn.action = action

    cell.content_view.add_subview(btn)

class Versions(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = create_cell(
            self, 
            row,
            lambda x,r: x.items[r]['name'])

        r = self.items[row]

        if r.get('startDate') and r.get('releaseDate'):

            from datetime import datetime 

            s = datetime.strptime(r['startDate'], "%Y-%M-%d")
            e = datetime.strptime(r['releaseDate'], "%Y-%M-%d")

            delta = e - s
            cell.detail_text_label.text = str(delta.days)

        create_button(
            cell, 
            "issues", 
            0.7, 
            lambda src: release_issues(
                src,
                tableview.project,
                tableview.data_source.items[row]['name']))

        create_button(
            cell, 
            "epics", 
            0.9, 
            lambda src: epics_page(
                src,
                tableview.project, 
                versions[tableview.project][row]['name']))

        return cell

class Releases(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = create_cell(self, row)

        create_button(
            cell, 
            "releases", 
            0.85, 
            lambda src: releases_page(
                src, 
                tableview.data_source.items[row]))

        return cell

@ui.in_background
@change_title
def releases_page(src, proj):

    if not versions.get(proj): 
        versions[proj] = jira.get_versions(proj)

    page = create_page(
        "Releases", 
        versions[proj],
        Versions) 
    
    page.allows_selection = False
    page.project = proj

    nav.push_view(page)

projects_page = create_page(
        "Products",[
        'RMADFE',
        'RMAZ',
        'QMMP'],
        Releases)

nav = ui.NavigationView(projects_page)
nav.present()
