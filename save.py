import keychain
import console
import base64
import requests

def get_credentials(svc):

	f = filter(
	lambda x: x[0] == svc,
	keychain.get_services())
	
	res = [x for x in f]
	
	if not res:
	
		usr, pwd = console.login_alert(svc)
		keychain.set_password(
		svc, usr, pwd)
		
		return usr, pwd
		
	return (res[0][1],
	keychain.get_password(*res[0]))
	
git_url = "https://api.github.com/repos/%s/%s?path=%s"
git_contents = "https://api.github.com/repos/%s/contents/%s"
git_repo = 'mikeplavsky/ios-pythonista'
	
def create_file(
	path,
	message,
	text):
		
	f = None
	
	try:
		f = get_file(path).json()
	except Exception as ex:
		print('first time save')
	
	git_user,git_key = get_credentials(git_repo)
	
	json = dict(
	message=message,
	content=str(base64.b64encode(text))[2:-1])
	
	if f:
		json['sha'] = f['sha']
		
	print('Saving to github')
	
	res = requests.put(
	
	git_contents % (git_repo,path),
	auth=(git_user,git_key),
	json=json)
	
	res.raise_for_status()
	return res
	
def get_file(path): 
	
	git_user,git_key = get_credentials(git_repo)

	res = requests.get(

		git_contents % (git_repo,path),
		auth=(git_user,git_key))

	res.raise_for_status()
	return res

def save_file(path, msg):
	
	with open(path) as f:
		s = f.read()
		create_file(path, msg, s.encode())
		
	print('Done.')

