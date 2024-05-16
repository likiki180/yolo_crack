import requests
import base64

# 服务器的地址
url = "http://localhost:5000/predict"

# 图片的路径
filepath = "inference/images/zj.jpg"

# 打开图片文件
file = open(filepath, "rb")

# 发送POST请求
response = requests.post(url, files={"image": file})

# 关闭文件
file.close()

# 解析服务器返回的 JSON 数据
data = response.json()

# 提取图像数据并解码
image_data = base64.b64decode(data['data']['image'])

# 写入到文件
with open('检测结果.jpg', 'wb') as f:
    f.write(image_data)

# 输出服务器的响应
print(data)
