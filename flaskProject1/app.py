from flask import Flask, jsonify, request, json
from hollistic import segmentation
from model import send_to_model
from data_score import score
from random import sample
import statistics
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
            segmentation()
            piece = send_to_model()
            list1 = ['Zara', 'Shein', 'Natura']
            brand=sample(list1,1)
            n1=score(piece[0], brand)
            brand = sample(list1, 1)
            n2=score(piece[1], brand)
            brand = sample(list1, 1)
            n3=score(piece[2], brand)
            scores=[n1, n2, n3]

            Result = []
            for scr in scores:
                Result.append(
                    {
                        'Piece' : scr[0],
                        'Brand' : scr[1],
                        'Score' : scr[2],
                    }
                )

            return jsonify({'Results': Result})


if __name__ == '__main__':
    app.run()
