import os
import jira

jira.get_credentials = lambda _: (
        os.environ["JIRA_USER"], os.environ["JIRA_PWD"])

def test_jira():
    res = jira.enum_stories(2003)
    assert len(res) > 1
