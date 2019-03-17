import clipboard
import console
import sys
import webbrowser
import json

import jira
jira.set_credentials()

def main():
    
    data = json.loads(sys.argv[1])
    console.clear()

    func = getattr(jira, data['func'])
    
    all = func(data)
    res = '\n\n'.join(all)

    clipboard.set(res)
    webbrowser.open_new('shortcuts://run-shortcut?name=CreateANote')

if __name__ == '__main__':
    main()
