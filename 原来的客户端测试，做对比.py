import requests

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

# 输出服务器的响应
print(response.json())