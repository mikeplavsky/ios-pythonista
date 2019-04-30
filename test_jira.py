import os
import jira
from config import jira_user
import pytest

cmd = f"security find-generic-password -a {jira_user} -s jira -w"
jira_pwd = os.popen(cmd).read().strip()

jira.get_credentials = lambda _: (
        jira_user, 
        jira_pwd)

def test_get_sprint_features():

    given = jira.sprint_stories("RMAZ")
    fs, d_fs, ps, d_ps = jira.get_features(given) 

    assert fs > 0 
    assert ps > 0 
    assert d_fs >= 0 
    assert d_ps >= 0 

def test_sprint_stories():

    res = jira.sprint_stories("QMMP")
    assert len(res["issues"]) > 1

    i = res["issues"][0]
    assert i["key"].startswith("QMMP")
    assert i["fields"]["customfield_12004"][0].find("QMMP Sprint") != -1

    assert set(i["fields"].keys()) == set(
            ['summary', 'customfield_12004','resolution',
            'customfield_10303', 'fixVersions', 'status'])
        
def test_get_versions():
    res = jira.get_versions("RMAZ")
    assert len(res) > 1
    assert len(res[0]['name']) > 1

def test_get_versions_names():
    res = jira.get_versions_names(dict(project="RMADFE"))
    assert len(res) > 1
    assert "10.1" in set(res)

@pytest.mark.parametrize("all, status",[
    (False, set(["In Progress","Reopened"])),
    (True, set(["Deployed"]))])
def test_search_stories(all, status):
    res = jira.search_stories("QMMP", "UI", all)    
    i = res["issues"][0]
    assert i["fields"]["status"]["name"] in status 

def test_search():
    res = jira.search_for_stories(
        dict(
            project="RMADFE",
            text="driver",
            all=False))
    assert len(res) > 2
    assert res[0] == "Q: driver"

def test_query():
    res = jira.query("project = RMADFE AND fixVersion = latestReleasedVersion()")
    assert res['total'] > 100

def test_create_issue():

    data = dict(
            project='QMMP',
            text="test\n\ndelete me")

    key,url = jira.create_issue(data) 

    assert key != ''
    assert url != ''

    issue = jira.get_issue(key)

    assert issue['fields']['summary'] == 'test'
    assert issue['fields']['description'] == 'delete me'

    res = jira.delete_issue(key)
    assert res.status_code == 204

def test_epic():
    res = jira.search_for_stories(
        dict(
            project="RMADFE",
            text="Zero Touch",
            all=False))
    assert len(res) > 2

def test_get_all_epics():
    res = jira.get_all_epics("RMADFE")
    assert len(res) == 38

def test_get_epics():
    res = jira.get_epics("RMADFE", "10.1")
    assert len(res) == 13

@pytest.mark.parametrize("version, epic, num",[
    ("10.1", "Bare Metal Recovery", 16),
    (None, "Bare Metal Recovery", 230),
    ("10.1", "Zero Touch 1", 0)])
def test_epic_issues(version, epic, num):
    res = jira.get_epic_issues("RMADFE", version, epic)
    assert len(res['issues']) >= num

@pytest.mark.parametrize("version, count",[
    ("9.0.1", 50),
    ("10.0", 200),
    ("10.1", 30)])
def test_release_issues(version, count):
    res = jira.get_release_issues("RMADFE", version)
    assert len(res['issues']) > count

def test_done_release():

    issues = jira.get_release_issues("RMADFE", "10.0")
    fs, d_fs, ps, d_ps = jira.get_features(issues) 

    assert fs == d_fs
    assert ps == d_ps
