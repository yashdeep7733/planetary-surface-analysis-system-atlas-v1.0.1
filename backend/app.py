import io
from flask import Flask, jsonify, request
import numpy as np
import cv2
import base64
from flask_cors import CORS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ultralytics import YOLO
import math

model = YOLO("runs/detect/runs/crater_detector/weights/best.pt") # Loading the trained YOLO model for crater detection

app = Flask(__name__)
CORS(app) # Enabling CORS for the Flask app to allow cross-origin requests from the frontend

@app.route("/detect", methods=["POST"])
def detecting_craters():

    # Raw image -> Bytes -> Numpy array -> OpenCV image

    if "image" not in request.files: # Checking if the key "image" is present in the uploaded files
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files["image"] # Accessing the uploaded file using the key "image"

    image_bytes = file.read() # Reading the file as bytes

    np_image = np.frombuffer(image_bytes, np.uint8) # Converting bytes to a numpy array
    cv_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR) # Decoding the numpy array to an OpenCV image

    # now we have (height, width, channels) in cv_image

    results = model(cv_image) # Performing crater detection on the OpenCV image using the YOLO model. The results will contain the detected objects and their bounding boxes.
    result = results[0] # Accessing the first result from the list of results returned by the YOLO model. This result contains the detected objects and their bounding boxes.

    annotated_image = result.plot() # Plotting the detected objects on the original image. The annotated_image will contain the original image with bounding boxes drawn around the detected craters.
    # YOLO gives .plot() method to visualize the results on the image. It returns an image with bounding boxes drawn around the detected objects.

    jpg_image_annotated = cv2.imencode(".jpg", annotated_image)[1].tobytes() # Encoding the annotated image to JPEG format and converting it to bytes
    base64_image_annotated = base64.b64encode(jpg_image_annotated).decode("utf-8") # Encoding the JPEG bytes to base64 format for easy transmission over HTTP

    crater_diameters = [] # Initializing an empty list to store the average sizes of the detected bounding boxes

    for box in result.boxes: # Iterating over the detected bounding boxes in the result
        x1, y1, x2, y2 = box.xyxy[0] # Extracting the coordinates of the bounding box (top-left and bottom-right corners)
        width = x2 - x1 # Calculating the width of the bounding box
        height = y2 - y1 # Calculating the height of the bounding box
        estimated_diameter = (width + height) / 2 # Calculating the average size of the bounding box
        crater_diameters.append(estimated_diameter) # Appending the average size to the list

    # Plotting the histogram of crater diameters using matplotlib to visualize the distribution of detected crater sizes. 
    # And return to React frontend to display the histogram of crater diameters.
    plt.figure(figsize=(8, 5))
    plt.hist(crater_diameters, bins=20, color='blue', edgecolor='black') # Creating a histogram with 20 bins, blue color, and black edges for the bars
    plt.xlabel('Crater Diameter')
    plt.ylabel('Frequency')
    plt.title('Distribution of Crater Diameters')
    # plt.savefig('./Example_histogram/crater_diameter_histogram.png') # Saving the histogram as an image file
    # Save plot to memory buffer instead of file
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    # Encode to base64
    histogram_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return jsonify({
        "crater_count": len(result.boxes), # Returning the number of detected craters in the image. The length of result.boxes gives the count of detected objects.
        "largest_crater_diameter": math.ceil(max(crater_diameters)) if crater_diameters else 0, # Returning the diameter of the largest detected crater. If no craters are detected, it returns 0.
        "average_crater_diameter": math.ceil(sum(crater_diameters) / len(crater_diameters)) if crater_diameters else 0, # Returning the average diameter of the detected craters. If no craters are detected, it returns 0.
        "smallest_crater_diameter": math.ceil(min(crater_diameters)) if crater_diameters else 0, # Returning the diameter of the smallest detected crater. If no craters are detected, it returns 0.
        "annotated_image": base64_image_annotated,  # Returning the base64 encoded annotated image with bounding boxes drawn around the detected craters.
        "histogram": histogram_base64  # Returning the base64 encoded histogram image.
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8600)
