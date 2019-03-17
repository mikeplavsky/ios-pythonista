import requests as r
from requests.auth import HTTPBasicAuth

from config import jira_host
import json

get_credentials = None

def set_credentials():

    import jira 

    from save import get_credentials
    jira.get_credentials = get_credentials

def request_jira(method,url,json=None):
    
    usr, pwd = get_credentials('jira')
    
    res = method(
        url, 
        auth=HTTPBasicAuth(usr,pwd),
        json=json)
        
    print(f'{method.__name__} {url} ...')
    res.raise_for_status()
    print('done.')
    
    return res

def get_jira(url):
    return request_jira(r.get,url).json()

status = lambda x: x['fields']['status']['name']

def sprints(v):

    s = v['fields']['customfield_12004']
    if not s: 
        return 'no sprints'

    def search(i): 
        import re
        r = re.search(r"Sprint ([\d]*)", i)
        return r.groups()[0]

    return ",".join(
        [search(i) for i in s]) 

def story_points(v):
    s = v['fields']['customfield_10303']
    
    if s:
        n = int(s)
        pts = "point" if n == 1 else "points"
        return f"{n} {pts}" 

    return 'not estimated'

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
        f"{sprints(v)}",
        f"{story_points(v)}"]) 

fmt_issues = lambda x: [fmt(v) for v in x['issues']]

def query(q, max_results=1000, error_if_more=False):

    url = f'https://{jira_host}/rest/api/latest/search?'

    query = dict(
        jql=q,
        maxResults=max_results,
        fields=[
            "key",
            "summary",
            "status",
            "customfield_12004", # must be taken from issue/editmeta
            "fixVersions",
            "customfield_10303"])

    res = request_jira(r.post, url, query).json()
    if error_if_more:
        assert res['maxResults'] < max_results
    
    return res

def sprint_stories(project):

    q = (
        f"project={project} AND "
        "sprint in openSprints() AND "
        "type not in subTaskIssueTypes() ORDER BY "
        "resolution DESC" )
    return query(q)

def enum_stories(data):
    
    res = sprint_stories(data['project']) 
    return fmt_issues(res) 

def search_stories(project, text, all):

    not_closed = "" if all else "AND resolution = Unresolved"

    jql=(
        f"project={project} {not_closed} AND "
        f"(summary ~ '{text}' OR description ~ '{text}') ORDER BY "
        "status DESC")
    return query(jql, max_results=20)

def search_for_stories(data):

    res = search_stories(
        data['project'], 
        data['text'], 
        data['all'])

    all = fmt_issues(res) 
    all.insert(0,f"Q: {data['text']}")

    return all
    
def get_versions(project):
    
    url = f'https://{jira_host}/rest/api/latest/project/{project}/version'

    res = request_jira(r.get, url).json()
    return [v for v in res['values'] if not v["released"]]
    
def get_versions_names(data):
    res = get_versions(data['project'])
    return [r['name'] for r in res]

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
    
    
        
    
