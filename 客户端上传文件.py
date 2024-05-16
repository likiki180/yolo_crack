import requests

url = "http://123.147.249.49/upload"  # replace 'your-server-ip' with your server's IP
file_path = "B1DE75A56D7680410662DAA0EEE38C61.txt"  # replace with the path to the file you want to upload

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(response.json())
