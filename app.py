from flask import Flask
from flask import Response

import jira
import json

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if app.config["DEBUG"]:
    
    print('in debug mode.')

    from config import jira_user
    import os

    cmd = f"security find-generic-password -a {jira_user} -s jira -w"
    jira_pwd = os.popen(cmd).read().strip()

    jira.get_credentials = lambda _: (
            jira_user, 
            jira_pwd)
else:
    
    jira.set_credentials()

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/api/product/<product>/versions')
def versions(product):
    
    res = jira.get_versions(product)
    txt = json.dumps(res)

    resp = Response(txt,mimetype='application/json')
    return resp

app.run('localhost', 8080, debug=True, use_reloader=False)
