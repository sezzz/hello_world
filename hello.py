from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/imgs')
def img():
    return send_file('imgs/welcome.jpg', mimetype='image/jpg')
@app.route('/imgs/welcome.jpg')
def imgs():
    return send_file('imgs/welcome.jpg', mimetype='image/jpg')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
