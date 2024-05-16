import base64
import io
import detect2  #新的检测脚本
from PIL import Image

from flask import Flask, request, jsonify
import torch
import os


app = Flask(__name__)


save_path = './inference/output/zj.jpg'
image_dir = './inference/images'  # directory where images will be saved

# @app.route('/predict', methods=["POST"])
# def predict():
#     if request.method != "POST":
#         return jsonify({"code": 2, "msg": "the request method is error!", "data": {"isSecret": "null"}})
#     if request.files.get("image"):
#         # 将读取的图片流转换为图片格式
#         im_file = request.files["image"]
#         im_bytes = im_file.read()
#         im = Image.open(io.BytesIO(im_bytes))
#
#         # Save the image
#         image_path = os.path.join(image_dir, im_file.filename)
#         im.save(image_path)
#
#         # Now we call the detect function from your script
#         result = detect2.run_detection(image_path)  # adjust parameters as needed
#
#         img_res = ''
#         with open(save_path, 'rb') as f:
#             img_res = f.read()
#             img_res = base64.b64encode(img_res)
#
#         return jsonify({"data": {"detect_res": "yes", "image": str(img_res, 'utf-8')}})

#
@app.route('/predict', methods=["POST"])
def predict():
    if request.method != "POST":
        return jsonify({"code": 2, "msg": "the request method is error!", "data": {"isSecret": "null"}})
    if request.files.get("image"):
        # 将读取的图片流转换为图片格式
        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        # 将图片输入到模型中，输出的结果是一个list，带有坐标类别等信息
        results = model(im, size=640)  # reduce size=320 for faster inference
        # 预测的结果（坐标 种类 置信度）
        result = results.pandas().xyxy[0].to_json(orient="records")

        img_res = ''
        with open(save_path, 'rb') as f:
            img_res = f.read()
            img_res = base64.b64encode(img_res)

        return jsonify({"data": {"detect_res": "yes", "image": str(img_res, 'utf-8')}})








# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             return jsonify({"code": 2, "msg": "No file part in the request.", "data": {"isSecret": "null"}})
#         file = request.files['file']
#
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             return jsonify({"code": 2, "msg": "No selected file.", "data": {"isSecret": "null"}})
#
#         file_path = os.path.join("/var/www/html/.well-known/pki-validation/", file.filename)
#
#         # Save the file to the specific directory
#         file.save(file_path)
#         return jsonify({"code": 0, "msg": "File uploaded successfully.", "data": {"isSecret": "null"}})



@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    return 'Success', 200



if __name__ == "__main__":
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    model = torch.hub.load("ultralytics/yolov5", "custom", path="weights/IMSC/last_95_640_16.pt", source="local",
                           force_reload=False)
    #第一个参数是要找到yolo5文件夹下面的hubconf.py文件  所以我们来调整一下服务器脚本的位置
    app.run(host='0.0.0.0', port=5000)