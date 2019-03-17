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
    shortcut = data.get('shortcut')
    
    url = f'shortcuts://run-shortcut?name={shortcut}' if shortcut else 'shortcuts://'
    
    all = func(data)
    res = '\n\n'.join(all)

    clipboard.set(res)
    webbrowser.open_new(url)

if __name__ == '__main__':
    main()
