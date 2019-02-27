import clipboard
import console
import sys
import webbrowser
import json

from jira import enum_stories

def main():
    
    project = json.loads(sys.argv[1])
    console.clear()
    
    print(project)
    
    enum_stories(
        project['project'],
        project['status'])
    
    webbrowser.open_new('shortcuts://run-shortcut?name=CreateANote')

if __name__ == '__main__':
    main()
