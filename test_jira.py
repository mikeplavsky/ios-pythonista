import os
import jira
from config import jira_user

cmd = f"security find-generic-password -a {jira_user} -s jira -w"
jira_pwd = os.popen(cmd).read().strip()

jira.get_credentials = lambda _: (
        jira_user, 
        jira_pwd)

def test_sprint_stories():

    res = jira.sprint_stories("QMMP")
    assert len(res["issues"]) > 1

    i = res["issues"][0]
    assert i["key"].startswith("QMMP")

    assert set(i["fields"].keys()) == set(
            ['summary', 'customfield_10303', 'fixVersions', 'status'])
        
def test_get_versions():
    res = jira.get_versions("RMAZ")
    assert len(res) > 1

def test_search():
    res = jira.search_for_stories("RMADFE","driver")
    assert len(res) > 1
