from flask import Flask, request, jsonify
from PIL import Image
import io
import torch
from torchvision import transforms
from models.experimental import attempt_load
from utils.general import non_max_suppression  # Add this line

...

app = Flask(__name__)

DETECTION_URL = "/predict"  # Specify your API endpoint

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model(weights_path='weights/IMSC/last_95_640_16.pt'):
    model = attempt_load(weights_path, map_location=device)
    return model

# Prepare the image
prepare_image = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to the size that your model expects
    transforms.ToTensor(),  # Convert the PIL Image to a tensor
    transforms.Normalize(  # Normalize the image
        mean=[0.485, 0.456, 0.406],  # These are RGB mean+std values
        std=[0.229, 0.224, 0.225]  # they come from the ImageNet dataset
    )
])

def detect(model, im, conf_thres=0.25, iou_thres=0.45):
    model.eval()  # Switch the model to evaluation mode
    im = im.to(device)  # Move the image tensor to the same device as the model
    im = im.unsqueeze(0)  # Add batch dimension

    with torch.no_grad():  # Disable gradient calculation
        results = model(im)[0]  # Only keep the predictions
        # Apply NMS
        results = non_max_suppression(results, conf_thres, iou_thres)

    detections = []
    for detection in results[0]:
        # Each detection is a tensor of the form [x1, y1, x2, y2, objectness, class]
        detections.append({
            'x1': detection[0].item(),
            'y1': detection[1].item(),
            'x2': detection[2].item(),
            'y2': detection[3].item(),
            'objectness': detection[4].item(),
            'class': detection[5].item(),
        })

    model.train()  # Switch the model back to training mode

    return detections



@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if request.method != "POST":
        return jsonify({"code": 2, "msg": "the request method is error!", "data": {"isSecret": "null"}})
    if request.files.get("image"):
        # Read the image file
        im_file = request.files["image"]
        im_bytes = im_file.read()
        # Convert to PIL Image
        im = Image.open(io.BytesIO(im_bytes))
        # Prepare the image
        im = prepare_image(im)
        result = detect(model, im)
        return jsonify({ "data": {"detect_res": "yes", "result": result}})

@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    return 'Success', 200

if __name__ == "__main__":
    model = load_model()
    app.run(host='0.0.0.0', port=5000)  # Specify your desired host and port
