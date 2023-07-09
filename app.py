from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/getDatabase', methods=['post'])
def getDatabase():
    return "Hello World"


@app.post('/api/imageRec')
def imageRec():
    file = request.files['file']
    # file should be an image

    # return format:
    # return jsonify({'msg': '{content of image}'})
    return


if __name__ == '__main__':
    app.run()
