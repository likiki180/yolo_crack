# backend.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    return 'Success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
