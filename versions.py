import ui

versions = dict()
epics = dict()

def create_page(name, data,source):

    page = ui.TableView()
    page.allows_selection = False

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
def sprint_issues(src, project):

    issues = jira.sprint_stories(project) 

    all = jira.fmt_issues(issues)

    all.insert(0,
        jira.get_features_header(issues))

    all.insert(
        0,
        f"{project}")

    create_note(all)

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
        f"{project}, {version}, {epic}" if version else f"{project}, {epic}")

    create_note(all)

def add_velocity_and_features(all, issues, done):

    fs, d_fs, ps, d_ps = jira.get_features(issues) 

    velocity = d_ps / done if done > 0 else 0
    projection = (ps - d_ps) / velocity if velocity else 0
    
    velocity_header = f"Velocity: {velocity * 10:.1f}"
    
    if projection:
    
        velocity_header = (
            f"Velocity: {velocity * 10:.1f}\n"
            f"Points: {ps - d_ps}\n"
            f"Projection: {projection:.0f}\n"
            f"Sprints: {projection/10:.0f}"
        )
    
    fs_header = (
        f"Features: {d_fs}\n"
        f"Points: {d_ps}") 
        
    if projection:

        fs_header = (
            f"Features: {d_fs} of {fs}\n"
            f"Points: {d_ps} of {ps}")

    all.insert(0,velocity_header)
    all.insert(0,fs_header)

    return velocity, projection

@ui.in_background
@change_title
def velocity_issues(src, project, days):

    issues = jira.get_done_issues(
        project,
        days) 

    all = jira.fmt_issues(issues)
    add_velocity_and_features(all, issues, days)

    all.insert(
        0,
        f"{project}, {days} days")

    create_note(all)

@ui.in_background
@change_title
def release_issues(src, project, version, dates):

    issues = jira.get_release_issues(
        project,
        version) 

    all = jira.fmt_issues(issues)
    add_velocity_and_features(all, issues, dates[2])

    if dates: 
        all.insert(0, dates_text(*dates))

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
                getattr(tableview,"version",None),
                tableview.data_source.items[row]))

        return cell

@ui.in_background
@change_title
def epics_page(src, project,version=None):

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

def release_dates(r):

    if not r.get('startDate') or not r.get('releaseDate'):
        return None

    from datetime import datetime 

    startDate = r['startDate']  
    releaseDate = r['releaseDate']  

    s = datetime.strptime(startDate, "%Y-%m-%d")
    e = datetime.strptime(releaseDate, "%Y-%m-%d")

    all = (e - s).days

    if e > datetime.now():
        e = datetime.now()

    done = (e - s).days if e > s else 0
    return (startDate, releaseDate, done, all)

def dates_text(startDate, releaseDate, done, all):

    text = (f"{startDate}\n"
            f"{releaseDate}\n")

    text += f"{done} of {all}" if all > done else f"{all}"
    return f"{text} days"

class Versions(ui.ListDataSource):

    def set_cell_text(self, cell, row):

        r = self.items[row]
        dates = release_dates(r)

        cell.detail_text_label.text = dates_text(*dates) if dates else ''
        cell.detail_text_label.number_of_lines = 0

        return r, dates

    def tableview_cell_for_row(self, tableview, section, row):

        cell = create_cell(
            self, 
            row,
            lambda x,r: x.items[r]['name'])

        r, dates = self.set_cell_text(cell, row)

        create_button(
            cell, 
            "issues", 
            0.7, 
            lambda src: release_issues(
                src,
                tableview.project,
                r['name'],
                dates))

        create_button(
            cell, 
            "epics", 
            0.9, 
            lambda src: epics_page(
                src,
                tableview.project, 
                r['name']))

        return cell

def more_about_project(src, project):

    import dialogs
    res = dialogs.list_dialog(
        items =
        ["Velocity", 
        "Epics"])

    if not res:
        return 

    if res == "Epics":
        epics_page(src, project)

    if res == "Velocity":
        velocity_issues(src,project,30)

class Releases(ui.ListDataSource):
    def tableview_cell_for_row(self, tableview, section, row):

        cell = create_cell(self, row)

        create_button(
            cell, 
            "sprint", 
            0.57, 
            lambda src: sprint_issues(
                src, 
                tableview.data_source.items[row]))

        create_button(
            cell, 
            "releases", 
            0.75, 
            lambda src: releases_page(
                src, 
                tableview.data_source.items[row]))

        create_button(
            cell, 
            "more", 
            0.92, 
            lambda src: more_about_project(
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
    
    page.project = proj
    nav.push_view(page)

if __name__ == '__main__':

    import jira
    jira.set_credentials()

    import clipboard
    import webbrowser

    projects_page = create_page(
            "Products",[
            'RMADFE',
            'RMAZ',
            'QMMP'],
            Releases)

    nav = ui.NavigationView(projects_page)
    nav.present()
