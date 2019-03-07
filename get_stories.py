import clipboard
import console
import sys
import webbrowser
import json

from jira import enum_stories

import jira
from save import get_credentials
jira.get_credentials = get_credentials

def main():
    
    project = json.loads(sys.argv[1])
    console.clear()
    
    all = enum_stories(
        project['project'])
    res = '\n\n'.join(all)

    clipboard.set(res)
    webbrowser.open_new('shortcuts://run-shortcut?name=CreateANote')

if __name__ == '__main__':
    main()
