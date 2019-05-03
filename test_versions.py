import os
import jira
from config import jira_user
from collections import UserDict

import ui_mock
import sys 
sys.modules['ui'] = ui_mock

import versions
versions.jira = jira

cmd = f"security find-generic-password -a {jira_user} -s jira -w"
jira_pwd = os.popen(cmd).read().strip()

jira.get_credentials = lambda _: (
        jira_user, 
        jira_pwd)

def test_change_title():

    res = []        
    func = versions.change_title(
            lambda src: res.append(src.title))

    src = UserDict()
    src.title = "Before"    

    func(src)

    assert src.title == "Before"
    assert res[0] == "..."

def test_create_button():

    class Button:
        def __init__(self, title):
            self.title = title            

    ui_mock.Button = Button

    cell = UserDict()
    cell.content_view = UserDict()

    cell.content_view.width = 1
    cell.content_view.height = 1

    res = []    
    cell.content_view.add_subview = lambda btn: res.append(btn)

    versions.create_button(cell, "Test", 1, "action")

    assert res[0].title == "Test" 
    assert res[0].action == "action" 

def mock_create_button():

    versions.create_cell = lambda x, y, _ = None: UserDict()    

    buttons = []
    versions.create_button = lambda x, y, z, _ : buttons.append(y)    

    return buttons
    
def test_versions_page():

    buttons = mock_create_button()

    sut = versions.Versions()
    sut.set_cell_text = lambda x,y: (None,None)

    sut.tableview_cell_for_row(None, None, None)

    assert set(buttons) == set(["epics","issues"])

def test_epics_page():

    buttons = mock_create_button()

    sut = versions.Epics()
    sut.tableview_cell_for_row(None, None, None)

    assert set(buttons) == set(["issues"])

def test_releases_page():

    buttons = mock_create_button()

    sut = versions.Releases()
    sut.tableview_cell_for_row(None, None, None)

    assert set(buttons) == set(["sprint", "releases", "more"])

def mock_create_note():

    src = UserDict()
    src.title = ""

    res = []    
    setattr(versions, "create_note", lambda s: res.extend(s))

    return src, res
    
def test_sprint_issues():

    src, res = mock_create_note()    

    versions.sprint_issues(src,"RMAZ")
    assert res[0] == "RMAZ"

def test_velocity_issues():

    src, res = mock_create_note()    

    versions.velocity_issues(src,"RMAZ", 20)
    assert res[0] == "RMAZ, 20 days"

def test_epic_issues():

    src, res = mock_create_note()    

    versions.epic_issues(src,"RMAZ","1.4", "Devices")
    assert res[0] == "RMAZ, 1.4, Devices"

def test_release_issues():

    src, res = mock_create_note()    

    versions.release_issues(src,"RMAZ","1.4", [1,2,3,4])
    assert res[0] == "RMAZ, 1.4"

def test_velocity_header_days():

    issues = jira.get_done_issues("RMAZ", 10)
    res = []

    v,p = versions.add_velocity_and_features(res, issues, 10)

    assert res[0].find("of") == -1 
    assert v > 0
    assert p == 0

def test_velocity_header_release():

    issues = jira.get_release_issues("RMAZ","1.4")
    res = []

    v, p = versions.add_velocity_and_features(res, issues, 1)

    assert res[0].find("of") != -1
    assert v > 0
    assert p > 0

def test_no_release_dates():

    res = versions.release_dates(dict())
    assert res == None

def test_release_dates():

    r = dict(
        startDate='2019-02-20',
        releaseDate='2019-10-31')

    res = versions.release_dates(r)

    assert res[0] == r['startDate']
    assert res[1] == r['releaseDate']
    assert res[3] == 253

def test_dates_text():

    i = ('2019','2020',2,5)
    res = versions.dates_text(*i)

    assert res.find('2 of 5') != -1