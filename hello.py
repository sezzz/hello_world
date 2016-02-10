from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/img')
def img():
    return send_file('img/vm1.png', mimetype='image/png')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
