import requests as r
from requests.auth import HTTPBasicAuth

from save import get_credentials
from config import jira_host

import webbrowser
import json

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
	
	res = request_jira(r.post, url, issue)
	key = res['key']
	
	return f'https://{jira_host}/browse/{key}'
	
	
		
	
