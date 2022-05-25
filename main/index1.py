from datetime import datetime
from pathlib import Path
import datetime
from flask import Flask, jsonify, request, render_template
from PIL import Image
import os
from pymongo import MongoClient
# 토치 관련 임포트
from app import imshow, transforms_test, class_names, inputs, labels, device
import torch
from torch import nn
from torchvision import models

SECRET_KEY = 'SPARTA'
client = MongoClient('localhost', 27017)
db = client.object


app = Flask(__name__)


# @app.route('/')
# def main():
#     # return render_template('index.html')
#     return 'Hello World!'


# model = models.resnet34(pretrained=True)
# num_ftrs = model.fc.in_features
# model.fc = nn.Linear(num_ftrs, 3)

# model.load_state_dict(torch.load('model_weighs.pth'))
# model.eval()

# model = torch.load('model3.pth')
# print(model)


@app.route('/upload', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        file = request.files['file']
        # file = request.files['file', False]
        extension = file.filename.split('.')[-1]
        today = datetime.datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{mytime}.{extension}'
        save_to = f'/static/img/{filename}'
        test = os.path.abspath(__file__)
        print(test)
        parent_path = Path(test).parent
        print(parent_path)
        abs_path = str(parent_path) + save_to
        print("abs_path", end=""), print(abs_path)
        file.save(abs_path)
        image = Image.open(abs_path)
        image = transforms_test(image).unsqueeze(0).to(device)
        post_list = list(db.posts.find({}))
        count = len(post_list) + 1

        doc = {
            'num': count,
            'file': f'/{filename}.{extension}',
            'create_time': mytime
        }
        db.posts.insert_one(doc)

        with torch.no_grad():
            outputs = model(image)
            _, preds = torch.max(outputs, 1)
            print(class_names[preds[0]])  # 예측 결과
            # print(
            #     f'[ 닮은 꼴: {class_names[preds[0]]}] (실제 정답: {class_names[labels.data[0]]})')                                  
            imshow(inputs.cpu().data[0],
                   title='예측 결과: ' + class_names[preds[0]])

        return jsonify({'class_name': "zd"})


if __name__ == '__main__':
    # model = models.resnet34(pretrained=True)
    model = torch.load('model.pth')
    app.run(host='0.0.0.0', port=5000, debug=True)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)