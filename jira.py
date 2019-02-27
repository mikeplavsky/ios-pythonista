import requests as r
from requests.auth import HTTPBasicAuth

from save import get_credentials
from config import jira_host

import webbrowser
import json
import clipboard

import appex

def log(str):
    if appex.is_running_extension():
        return
    print(str)
    
def request_jira(method,url,json=None):
    
    usr, pwd = get_credentials('jira')
    
    res = method(
        url, 
        auth=HTTPBasicAuth(usr,pwd),
        json=json)
        
    log(f'{method.__name__} {url} ...')
    res.raise_for_status()
    log('done.')
    
    return res

def get_jira(url):
    return request_jira(r.get,url).json()

def get_curr_sprint(board_id):
    
    url = f'https://{jira_host}/rest/agile/latest/board/{board_id}/sprint?state=active'
    return get_jira(url)['values'][0]
    
def get_curr_stories(board_id):
    
    sprint = get_curr_sprint(board_id)['id']
    url = f'https://{jira_host}/rest/agile/latest/board/{board_id}/sprint/{sprint}/issue'
    
    return get_jira(url)
    
def enum_stories(board_id, s=''):
    
    issues = get_curr_stories(board_id)['issues']
    
    subtask = lambda x: x['fields']['issuetype']['subtask']
    status = lambda x: x['fields']['status']['name']
    in_status = lambda x: True if not s else status(x) == s

    all = [f"{v['fields']['summary']}\nhttps://{jira_host}/browse/{v['key']}" for _,v in enumerate(issues) if not subtask(v) and in_status(v)]
    
    res = '\n\n'.join(all)
    print(res)
    
    clipboard.set(res)
    
    
def get_versions(project):
    
    url = f'https://{jira_host}/rest/api/latest/project/{project}/version'

    res = request_jira(r.get, url).json()
    [print(v['name']) for v in res['values']]
    
def delete_issue(key):
    
    url = f'https://{jira_host}/rest/api/latest/issue/{key}'
    return request_jira(r.delete, url)
    
def get_issue(key):
    
    url = f'https://{jira_host}/rest/api/latest/issue/{key}'

    res = request_jira(r.get, url).json()
    fs = res['fields']
    
    print(
        f"\n{fs['summary']}\n\n{fs['description']}")
        
    return res

def create_issue(
    project,
    summary,
    description=''):
    
    issue = dict(
        fields=dict(
            project=dict(key=f'{project}'),
            summary=f'{summary}',
            description=f'{description}',
            issuetype=dict(name='Story')))
    
    url = f'https://{jira_host}/rest/api/latest/issue/'
    
    res = request_jira(
        r.post, url, issue).json()
    key = res['key']
    
    return f'https://{jira_host}/browse/{key}'
    
    
        
    
