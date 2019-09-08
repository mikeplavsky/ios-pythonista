from flask import Flask
from flask import Response, request

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

    jira.get_credentials = lambda _: (
            os.environ['JIRA_USER'], 
            os.environ['JIRA_PWD'])

else:
    
    jira.set_credentials()

def response(res):

    resp = Response(
        json.dumps(res),
        mimetype='application/json')

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/query', methods=['POST'])
def query():

    data = json.loads(request.data)

    stories = jira.search_stories(
        data['product'],
        data['query'],
        True)
    
    return response(stories)

@app.route('/api/stories', methods=['POST'])
def stories():

    data = json.loads(request.data)

    stories = jira.get_epic_issues(
        data['product'],
        data['release'],
        data['epic'])
    
    return response(stories)

@app.route('/api/products')
def products():

    products = os.environ['JIRA_PRODUCTS']
    return response(
        [dict(name=x) for x in products.split(',')])

@app.route('/api/products/<product>/sprint')
def sprint(product):
    return response(
        jira.sprint_stories(product))

@app.route('/api/products/<pruduct>/releases/<release>/epics')
def release_epics(product,release):

    epics = jira.get_epics(
        product, release)
    
    return response(epics)

@app.route('/api/products/<product>/releases/<release>/epics/<path:epic>')
def epic_stats(product,release,epic):

    print(product)
    print(release)
    print(epic)

    issues = jira.get_epic_issues(
        product, release, epic)

    res = jira.get_features(issues)

    return response(
        dict(
            features = res[0],
            done_features = res[1],
            points = res[2],
            done_points = res[3]))

@app.route('/api/products/<product>/releases/<release>')
def release_stats(product,release):

    issues = jira.get_release_issues(
        product, release)

    res = jira.get_features(issues)

    return response(
        dict(
            features = res[0],
            done_features = res[1],
            points = res[2],
            done_points = res[3]))
    

@app.route('/api/products/<product>/features/done')
def done_stats(product):
    
    days = 30

    issues = jira.get_done_issues(product, days)
    res = jira.get_features(issues)

    velocity = round(res[2] / days * 10,1)

    return response(
        dict(velocity=velocity,
            features=res[0],
            points = res[2]))

@app.route('/api/products/<product>/versions')
def versions(product):
    
    return response(
        jira.get_versions(product))

@app.route('/')
@app.route('/products/<path:path>')
@app.route('/products')
def product(path=''):
    return app.send_static_file('index.html')

if  __name__ == '__main__':
    app.run('localhost', 8080, debug=False, use_reloader=False, threaded=True)
