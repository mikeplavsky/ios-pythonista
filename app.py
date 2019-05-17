from flask import Flask
from flask import Response

import jira
import json

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

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

def response(res):

    resp = Response(
        json.dumps(res),
        mimetype='application/json')

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/product/<product>/features/done')
def done_features(product):
    
    issues = jira.get_done_issues(product, 30)
    res = jira.get_features(issues)

    return response(
        dict(features=res[0], points = res[2]))

@app.route('/api/product/<product>/versions')
def versions(product):
    
    return response(
        jira.get_versions(product))

@app.route('/')
@app.route('/product/<path:path>')
@app.route('/products')
def product(path=''):
    return app.send_static_file('index.html')

app.run('localhost', 8080, debug=False, use_reloader=False)
