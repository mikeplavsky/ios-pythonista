import requests as r
from requests.auth import HTTPBasicAuth

from config import jira_host
import json

get_credentials = None

def log(str):
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
    
status = lambda x: x['fields']['status']['name']

def story_points(v):
    s = v['fields']['customfield_10303']
    return f"{int(s)} points" if s else 'not estimated'

def versions(v):
    vs = v['fields']['fixVersions']
    if vs:
        return ','.join([x['name'] for x in vs])
    else:
        return 'no releases'

def fmt (v): 
    return '\n'.join([
        f"{v['fields']['summary']}",
        f"https://{jira_host}/browse/{v['key']}",
        f"{status(v)}",
        f"{versions(v)}",
        f"{story_points(v)}"]) 

def enum_stories(board_id, s=''):
    
    issues = get_curr_stories(board_id)['issues']
    
    subtask = lambda x: x['fields']['issuetype']['subtask']
    in_status = lambda x: True if not s else status(x) == s

    res = sorted(issues, key=status)
    return [fmt(v) for v in res if not subtask(v) and in_status(v)]

def search_for_stories(project, text, all=False):

    url = f'https://{jira_host}/rest/api/latest/search?'
    not_closed = "" if all else "AND status != Closed"

    query = dict(
        jql=f"project={project} {not_closed} AND (summary ~ '{text}' OR description ~ '{text}') ORDER BY status",
        fields=[
            "key",
            "summary",
            "status",
            "fixVersions",
            "customfield_10303"])

    res = request_jira(
        r.post, url, query).json()

    return [fmt(v) for v in res['issues']]
    
def get_versions(project):
    
    url = f'https://{jira_host}/rest/api/latest/project/{project}/version'

    res = request_jira(r.get, url).json()
    return [v for v in res['values'] if not v["released"]]
    
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
    
    
        
    
