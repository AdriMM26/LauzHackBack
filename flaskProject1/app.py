from flask import Flask, jsonify, request, json

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World!"


@app.route('/api/image', methods=['POST'])
def getImage():
    import base64

    if request.data == None:
        return jsonify({'message': 'ERROR while getting image'})
    else:
        bodyParsed = json.loads(request.data)
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(bodyParsed["image"]))
            j_data = json.dump(fd.read())
            print("Your image is loading")
            r=requests.post()
            return r



if __name__ == '__main__':
    app.run()
