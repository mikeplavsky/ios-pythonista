from flask import Flask
from flask import jsonify

import jira

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='')

if app.config["DEBUG"]:

    from config import jira_user
    import os

    cmd = f"security find-generic-password -a {jira_user} -s jira -w"
    jira_pwd = os.popen(cmd).read().strip()

    jira.get_credentials = lambda _: (
            jira_user, 
            jira_pwd)

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/api/versions')
def versions():
    res = jira.get_versions("RMADFE")
    return jsonify(res)

app.run('localhost', 8080, debug=False)
