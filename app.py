from flask import Flask, request, jsonify
import requests
import os
import csv
from dotenv import load_dotenv
from PIL import Image,ImageDraw
from io import BytesIO
from roboflow import Roboflow
from models import Prediction  # Import the Prediction class
from utils import update_predictions, calculate_total_price, load_prices, preprocess  # Import functions from utils.py
from ultralytics import YOLO
# Load environment variables from .env file
load_dotenv()

app = Flask("waste_model")

# Retrieve API key and model endpoint from environment variables
ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY')
PROJECT_MODEL = os.getenv('PROJECT_MODEL')
MODEL_VERSION=os.getenv('MODEL_VERSION')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an image file is included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    # Retrieve the image file from the request
    file = request.files['file']

    # Preprocess the image
    img_byte_arr, original_width, original_height = preprocess(file)
    
    # If there was an error during preprocessing, return the error message
    if img_byte_arr is None:
        return jsonify({"error": f"Error processing image: {original_height}"}), 400

    # Send the preprocessed image to the Roboflow API
    # rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    # project = rf.workspace().project(PROJECT_MODEL)
    # model = project.version(MODEL_VERSION).model
    # predictions_data = model.predict("image.jpg", confidence=20, overlap=30).json()
    predictions_list = []

    # Load the model
    model = YOLO('./model/best.pt')

    # Perform inference
    results = model.predict(source="image.jpg",conf=0.02, save=True, device='cpu')

    # Access detection results
    for result in results:
            for idx in range(len(result.boxes.cls)):  # Loop through each detection (for multiple boxes)
                class_idx = int(result.boxes.cls[idx].item())  # Get the index of the class
                class_name = result.names[class_idx]  # Get the class name using the class index
                
                # Create the Prediction object (you may need to fetch the correct price later)
                prediction = Prediction(classe=class_name, price_ex_vat=0, price_inc_vat=0)
                predictions_list.append(prediction)

    # for pred in predictions_data['predictions']:
    #         prediction = Prediction(
    #             x=pred['x'],
    #             y=pred['y'],
    #             width=pred['width'],
    #             height=pred['height'],
    #             confidence=pred['confidence'],
    #             class_name=pred['class'],
    #             class_id=pred['class_id'],
    #             detection_id=pred['detection_id'],
    #             image_path=pred['image_path']
    #         )
    #         predictions_list.append(prediction)
    
    prices = load_prices()

    predictions_list = update_predictions(predictions_list,prices)
    total_price = calculate_total_price(predictions_list, prices)

    # Prepare the image with bounding boxes
    # image = Image.open(file.stream)
    # image_with_bboxes = draw_bounding_boxes(image, predictions_list, original_width, original_height)

    # Save the image with bounding boxes to a byte buffer
    # img_byte_arr_with_bboxes = BytesIO()
    # image_with_bboxes.save(img_byte_arr_with_bboxes, format='JPEG')
    # img_byte_arr_with_bboxes.seek(0)

    response_data = {
            "total_price": total_price
        }
    detected_classes = [pred.to_dict() for pred in predictions_list]
    print(detected_classes)
    # Return total price as JSON and the image with bounding boxes
    return jsonify({"predictions": detected_classes, "total_price": total_price}), 200


if __name__ == '__main__':
    app.run(debug=False)