import appex
import clipboard
import console

from jira import create_issue
import sys

def create_story(
	project, 
	text):
	
	res = text.split('\n')
	
	summary = res[0]
	description = '\n'.join(res[2:])
	
	console.hud_alert(
		f'{project}: {summary}')
	
	res = create_issue(
		project, summary, description)
		
	clipboard.set(res)
	
	console.hud_alert(
		'Copied to clipboard')

def main():
	
	text = appex.get_text()
	
	if text:
		project = sys.argv[1]
		create_story(project, text)

if __name__ == '__main__':
	main()
