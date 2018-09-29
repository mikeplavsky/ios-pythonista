import requests as r
from requests.auth import HTTPBasicAuth

from save import get_credentials
from config import jira_host

def get_curr_sprint(board_id):
	
	jira_url = f'https://{jira_host}/rest/agile/latest/board/{board_id}/sprint?state=active'
	
	usr, pwd = get_credentials('jira')
	
	res = r.get(jira_url, 
		auth=HTTPBasicAuth(usr,pwd))
	return res 
