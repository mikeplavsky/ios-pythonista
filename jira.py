import requests as r
from requests.auth import HTTPBasicAuth

from save import get_credentials
from config import jira_host

import json

def request_jira(method,url,json=None):
	
	usr, pwd = get_credentials('jira')
	
	res = method(
		url, 
		auth=HTTPBasicAuth(usr,pwd),
		json=json)
		
	print(f'{method.__name__} {url} ...')
	res.raise_for_status()
	print('done.')
	
	return res.json()

def get_jira(url):
	return request_jira(r.get,url)

def get_curr_sprint(board_id):
	
	url = f'https://{jira_host}/rest/agile/latest/board/{board_id}/sprint?state=active'
	
	return get_jira(url)['values'][0]
	
def get_curr_stories(board_id):
	
	sprint = get_curr_sprint(board_id)['id']
	
	url = f'https://{jira_host}/rest/agile/latest/board/{board_id}/sprint/{sprint}/issue'
	
	return get_jira(url)
	
def enum_stories(board_id):
	res = get_curr_stories(board_id)['issues']
	for i,v in enumerate(res):
		print(f"{i+1}. {v['fields']['summary']}")
		

def create_issue(project):
	
	issue = dict(
		fields=dict(
			project=dict(key=f'{project}'),
			summary='test',
			description='',
			issuetype=dict(name='Story')))
			
	print(json.dumps(issue))
	
	url = f'https://{jira_host}/rest/api/latest/issue/'
	return request_jira(r.post, url, issue)
		
	
