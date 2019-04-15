import os
import jira
from config import jira_user
import pytest

import ui_mock
import sys 
sys.modules['ui'] = ui_mock

import versions

cmd = f"security find-generic-password -a {jira_user} -s jira -w"
jira_pwd = os.popen(cmd).read().strip()

jira.get_credentials = lambda _: (
        jira_user, 
        jira_pwd)

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