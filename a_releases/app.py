from flask import Flask
app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='')

@app.route('/')
def main():
    return app.send_static_file('index.html')

app.run('localhost', 8080, debug=False)
