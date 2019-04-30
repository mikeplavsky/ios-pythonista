import requests as r
from requests.auth import HTTPBasicAuth
from config import jira_host

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

def resolution(x): 

    res = x['fields']['resolution']
    return res['name'] if res else ''

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

points = lambda v: v['fields']['customfield_10303']

def story_points(v):
    s = points(v) 
    
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
            "resolution",
            "customfield_12004", # must be taken from issue/editmeta
            "fixVersions",
            "customfield_10303",
            "customfield_12301"])

    res = request_jira(r.post, url, query).json()
    if error_if_more:
        assert res['maxResults'] < max_results
    
    return res

def sprint_stories(project):

    q = (
        f"project={project} AND " "sprint in openSprints() AND "
        "type not in subTaskIssueTypes() ORDER BY "
        "resolution DESC" )
    return query(q)

done = lambda x: status(x) == 'Closed'
ps = lambda x: int(points(x)) if points(x) else 0

def get_features(res):

    issues = res['issues']
    return (
        len(issues),
        len([x for x in issues if done(x)]),
        sum(ps(x) for x in issues),
        sum(ps(x) for x in issues if done(x)))

def get_features_header(issues):

    fs, d_fs, ps, d_ps = get_features(issues)
    return (
        f"Features: {d_fs} of {fs}\n"
        f"Points: {d_ps} of {ps}")

def enum_stories(data):

    res = sprint_stories(data['project']) 

    issues = fmt_issues(res) 
    issues.insert(0, get_features_header(res))

    return issues

def search_stories(project, text, all):

    not_closed = "" if all else "AND resolution = Unresolved AND status != Closed"

    jql=(
        f"project={project} {not_closed} AND "
        f"(summary ~ '{text}' OR "
        f"description ~ '{text}' OR "
        f"issue in linkedIssuesFromQuery(\"'Epic Name' ~ '{text}'\")) ORDER BY "
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
    return [v for v in res['values']] #if not v["released"]]
    
def get_versions_names(data):
    res = get_versions(data['project'])
    return [r['name'] for r in res]

def get_all_epics(project):
    jql = (
        f'issue in epicsFromQuery('
        f'"project = {project}")'
    )
    res = query(jql)
    return sorted([x['fields']['customfield_12301'] for x in res['issues']])

def get_epics(project,version):
    jql = (
        f'issue in epicsFromQuery('
        f'"project = {project} AND '
        f'fixVersion = \'{version}\'")'
    )
    res = query(jql)
    return sorted([x['fields']['customfield_12301'] for x in res['issues']])

def get_release_issues(project,version):

    jql =  (
        f'project = "{project}" AND '
        f'fixVersion = "{version}" ORDER BY '
        f'resolution DESC'
    )
    return query(jql)

def get_epic_issues(project,version,epic):

    jql =  (
        f'issue in linkedIssuesFromQuery("\'Epic Name\' ~ \'{epic}\'") AND '
        f'project = "{project}"')

    if version:
        jql += f' AND fixVersion = "{version}" ' 
        
    jql += 'ORDER BY resolution DESC'
    return query(jql)

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

def create_issue(data):

    project = data['project']
    text = data['text']

    lines = text.split('\n')

    summary = lines[0]
    description = '\n'.join(lines[2:]) 
    
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
    
    return key, f'https://{jira_host}/browse/{key}'
    
    
        
    
