import base64
import io
import detect2#新的检测脚本
from PIL import Image
from flask import Flask, send_file

from flask import Flask, request, jsonify
import torch
import os


app = Flask(__name__)


save_path = './inference/output/zj.jpg'
image_dir = './inference/images'  # directory where images will be saved


@app.route('/predict', methods=["POST"])
def predict():
    if request.method != "POST":
        return jsonify({"code": 2, "msg": "the request method is error!", "data": {"isSecret": "null"}})
    if request.files.get("image"):
#第一大步 收到图像并且保存

        # 从HTTP请求中获取图像文件
        im_file = request.files["image"]
        print(type(im_file))
        # 读取图像文件的字节数据
        im_bytes = im_file.read()
        print(type(im_bytes))
        # 使用PIL库打开图像
        im = Image.open(io.BytesIO(im_bytes))
        print(type(im))
        # 转换并保存为.jpg格式
        save_path = 'shoudao.jpg'
        im.save(save_path, 'JPEG')
        print('收到')
#第二大步 检测图片并且保存

        detect2.run_detection(save_path)







#第三大步 返回检测结果给微信小程序

        image = Image.open('inference/output/shoudao.jpg')
        # 创建一个字节流对象
        byte_stream = io.BytesIO()
        # 将图像保存到字节流
        image.save(byte_stream, format='PNG')

        # 获取字节数据
        image_bytes = byte_stream.getvalue()

        # 将字节数据编码为base64字符串
        img_res = base64.b64encode(image_bytes)




        return jsonify({"data": {"detect_res": "yes", "image": str(img_res, 'utf-8')}})





@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    return 'Success', 200

#托管一个视频到服务器
@app.route('/video')
def video_file():
    return send_file('G:\\PythonProject\\pythonProject\\rddc2020\\yolov5\\inference\\output\\行车录屏.mp4', mimetype='video/mp4')


if __name__ == "__main__":
    app.run(port=5000)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
