from flask import Flask, jsonify, request, json
from hollistic import segmentation
from model import send_to_model
from data_score import score
import random
import numpy as np
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
        with open("./Images/imageToSave.png", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(bodyParsed["image"]))
            segmentation()
            piece = send_to_model()
            list1 = ['Zara', 'Shein', 'Natura']

            notas = []

            for cloth in piece:
                brand = random.choice(list1)
                points = score(cloth,brand)
                notas.append([cloth, brand, points])



            Result = []
            for scr in notas:
                Result.append(
                    {
                        'Piece' : scr[0],
                        'Brand' : scr[1],
                        'Score' : scr[2]
                    }
                )

            return jsonify({'Results': Result})


if __name__ == '__main__':
    app.run()
