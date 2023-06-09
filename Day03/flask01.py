# Flask Web Server
from flask import Flask

app = Flask(__name__)

@app.route('/') # http://localhost:5000/
def index():
    return ('hello flask!')

if __name__ == '__main__':
    app.run(host='localhost')