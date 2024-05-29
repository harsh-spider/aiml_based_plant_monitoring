from flask import Flask, request, render_template, jsonify
import numpy as np
import cv2
import pickle
from pathlib import Path
import time
import base64
from io import BytesIO
from PIL import Image
from utils import load_trained_model, prepare_image, prepare_frame
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_path = 'pred/model_cnn_1.h5'
model = load_trained_model(model_path)
label_binarizer = pickle.load(open('./pred/label_transform.pkl', 'rb'))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            logger.error("No file part in the request")
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return "No selected file"
        if file:
            file_path = f"./static/{file.filename}"
            file.save(file_path)
            image = prepare_image(file_path)
            predictions = predict_disease(image)
            probability = max(prediction['probability'] for prediction in predictions)  # Calculate max probability
            label = predictions[0]['disease']  # Get the disease label from the first prediction
            return render_template("result.html", predictions=predictions, file_path=file_path, probability=probability, label=label)
    return render_template("index.html")


def detect_leaf(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        leaf_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(leaf_contour)
        min_leaf_area = 3000
        print("Detected contour area:", area)  # Debug statement
        
        if area > min_leaf_area:
            print("Leaf detected")  # Debug statement
            return True
    print("No leaf detected")  # Debug statement
    return False

def predict_disease(image):
    result = model.predict(image)
    top_indices = result[0].argsort()[-5:][::-1]
    top_labels = label_binarizer.classes_[top_indices]
    top_probabilities = result[0][top_indices]
    predictions = [{"disease": label, "probability": float(prob)} for label, prob in zip(top_labels, top_probabilities)]
    return predictions

@app.route("/realtime", methods=['GET'])
def realtime():
    return render_template("realtime.html")

@app.route("/fertilizer_recommendation")
def fertilizer_recommendation():
    return render_template("fertilizer_recommendation.html")

@app.route("/capture", methods=['POST'])
def capture():
    try:
        data = request.json
        image_data = data['image']
        image_data = image_data.split(",")[1]
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        if detect_leaf(frame):
            logger.info("Leaf detected in the frame")
            image = prepare_frame(frame)
            predictions = predict_disease(image)
            output_dir = "static/output/"
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            output_path = Path(output_dir) / f"processed_image_{int(time.time())}.png"
            cv2.imwrite(str(output_path), frame)
            response = {'predictions': predictions, 'image_path': str(output_path)}
            return jsonify(response)
        else:
            logger.info("No leaf detected in the frame")
            return jsonify({'error': 'No leaf detected'})
    except Exception as e:
        logger.error(f"Error in /capture: {e}")
        return jsonify({'error': str(e)}), 500


@app.route("/get_fertilizer_recommendation", methods=['GET'])
def get_fertilizer_recommendation():
    disease_name = request.args.get('disease')
    fertilizer_recommendations = {
        '_Late_blight': 'Copper-based fungicide',
        '___Late_blight':'Copper-based fungicide',
        '_Early_blight': 'Potassium bicarbonate',
        'Spider_mites_Two_spotted_spider_mite': 'Insecticidal soap or neem oil',
        '__Target_Spot': 'Copper fungicide',
        '_Leaf_Mold':'10-10-10, organic compost, or foliar sprays like fish emulsion',
        '_Bacterial_spot': 'Copper-based fungicide or bactericide',
        '_mosaic_viruss': 'No specific fertilizer; focus on removing infected plants and controlling vectors',
        '_YellowLeaf__Curl_Virus': 'Nitrogen-rich fertilizer',
        # Add more recommendations as needed
    }
    recommendation = fertilizer_recommendations.get(disease_name, None)
    return jsonify({'recommendation': recommendation})


if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, request, render_template, jsonify
# import numpy as np
# import cv2
# import pickle
# from pathlib import Path
# import time
# import base64
# from io import BytesIO
# from PIL import Image
# from utils import load_trained_model, prepare_image, prepare_frame
# import logging

# app = Flask(__name__)

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# model_path = 'pred/model_cnn_1.h5'
# model = load_trained_model(model_path)
# label_binarizer = pickle.load(open('./pred/label_transform.pkl', 'rb'))




# # def detect_leaf(frame):
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
# #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# #     if contours:
# #         leaf_contour = max(contours, key=cv2.contourArea)
# #         area = cv2.contourArea(leaf_contour)
# #         min_leaf_area = 3000
# #         if area > min_leaf_area:
# #             return True
# #     return False

# def detect_leaf(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Adjust the threshold value (currently 150) as needed
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     if contours:
#         leaf_contour = max(contours, key=cv2.contourArea)
#         area = cv2.contourArea(leaf_contour)
#         min_leaf_area = 3000
#         print("Detected contour area:", area)  # Debug statement
        
#         if area > min_leaf_area:
#             print("Leaf detected")  # Debug statement
#             return True
#     print("No leaf detected")  # Debug statement
#     return False


# def predict_disease(image):
#     result = model.predict(image)
#     itemindex = np.where(result == np.max(result))
#     return label_binarizer.classes_[itemindex[1][0]], np.max(result)

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             logger.error("No file part in the request")
#             return "No file part"
#         file = request.files['file']
#         if file.filename == '':
#             logger.error("No selected file")
#             return "No selected file"
#         if file:
#             file_path = f"./static/{file.filename}"
#             file.save(file_path)
#             image = prepare_image(file_path)
#             label, probability = predict_disease(image)
#             return render_template("result.html", label=label, probability=probability, file_path=file_path)
#     return render_template("index.html")

# @app.route("/realtime", methods=['GET'])
# def realtime():
#     return render_template("realtime.html")

# # @app.route("/capture", methods=['POST'])
# # def capture():
# #     try:
# #         data = request.json
# #         image_data = data['image']
# #         image_data = image_data.split(",")[1]
# #         image = Image.open(BytesIO(base64.b64decode(image_data)))
# #         frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# #         if detect_leaf(frame):
# #             image = prepare_frame(frame)
# #             label, probability = predict_disease(image)
# #             output_dir = "static/output/"
# #             Path(output_dir).mkdir(parents=True, exist_ok=True)
# #             output_path = Path(output_dir) / f"processed_image_{int(time.time())}.png"
# #             cv2.imwrite(str(output_path), frame)
# #             response = {'disease': label, 'probability': float(probability), 'image_path': str(output_path)}
# #             return jsonify(response)
# #         else:
# #             logger.info("No leaf detected in the frame")
# #             return jsonify({'error': 'No leaf detected'}), 400
# #     except Exception as e:
# #         logger.error(f"Error in /capture: {e}")
# #         return jsonify({'error': str(e)}), 500


# @app.route("/capture", methods=['POST'])
# def capture():
#     try:
#         data = request.json
#         image_data = data['image']
#         image_data = image_data.split(",")[1]
#         image = Image.open(BytesIO(base64.b64decode(image_data)))
#         frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#         if detect_leaf(frame):
#             logger.info("Leaf detected in the frame")
#             image = prepare_frame(frame)
#             label, probability = predict_disease(image)
#             output_dir = "static/output/"
#             Path(output_dir).mkdir(parents=True, exist_ok=True)
#             output_path = Path(output_dir) / f"processed_image_{int(time.time())}.png"
#             cv2.imwrite(str(output_path), frame)
#             response = {'disease': label, 'probability': float(probability), 'image_path': str(output_path)}
#             return jsonify(response)
#         else:
#             logger.info("No leaf detected in the frame")
#             return jsonify({'error': 'No leaf detected'})
#     except Exception as e:
#         logger.error(f"Error in /capture: {e}")
#         return jsonify({'error': str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, request, render_template, jsonify
# import numpy as np
# import cv2
# import pickle
# from pathlib import Path
# import time
# import base64
# from io import BytesIO
# from PIL import Image
# from utils import load_trained_model, prepare_image, prepare_frame
# import logging

# app = Flask(__name__)

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# model_path = 'pred/model_cnn_1.h5'
# model = load_trained_model(model_path)
# label_binarizer = pickle.load(open('./pred/label_transform.pkl', 'rb'))

# def detect_leaf(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     if contours:
#         leaf_contour = max(contours, key=cv2.contourArea)
#         area = cv2.contourArea(leaf_contour)
#         min_leaf_area = 3000
#         print("Detected contour area:", area)  # Debug statement
        
#         if area > min_leaf_area:
#             print("Leaf detected")  # Debug statement
#             return True
#     print("No leaf detected")  # Debug statement
#     return False

# def predict_disease(image):
#     result = model.predict(image)
#     top_indices = result[0].argsort()[-5:][::-1]
#     top_labels = label_binarizer.classes_[top_indices]
#     top_probabilities = result[0][top_indices]
#     predictions = [{"disease": label, "probability": float(prob)} for label, prob in zip(top_labels, top_probabilities)]
#     return predictions

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             logger.error("No file part in the request")
#             return "No file part"
#         file = request.files['file']
#         if file.filename == '':
#             logger.error("No selected file")
#             return "No selected file"
#         if file:
#             file_path = f"./static/{file.filename}"
#             file.save(file_path)
#             image = prepare_image(file_path)
#             predictions = predict_disease(image)
#             return render_template("result.html", predictions=predictions, file_path=file_path)
#     return render_template("index.html")

# @app.route("/realtime", methods=['GET'])
# def realtime():
#     return render_template("realtime.html")

# @app.route("/fertilizer_recommendation")
# def fertilizer_recommendation():
#     return render_template("fertilizer_recommendation.html")

# @app.route("/capture", methods=['POST'])
# def capture():
#     try:
#         data = request.json
#         image_data = data['image']
#         image_data = image_data.split(",")[1]
#         image = Image.open(BytesIO(base64.b64decode(image_data)))
#         frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#         if detect_leaf(frame):
#             logger.info("Leaf detected in the frame")
#             image = prepare_frame(frame)
#             predictions = predict_disease(image)
#             output_dir = "static/output/"
#             Path(output_dir).mkdir(parents=True, exist_ok=True)
#             output_path = Path(output_dir) / f"processed_image_{int(time.time())}.png"
#             cv2.imwrite(str(output_path), frame)
#             response = {'predictions': predictions, 'image_path': str(output_path)}
#             return jsonify(response)
#         else:
#             logger.info("No leaf detected in the frame")
#             return jsonify({'error': 'No leaf detected'})
#     except Exception as e:
#         logger.error(f"Error in /capture: {e}")
#         return jsonify({'error': str(e)}), 500


# @app.route("/get_fertilizer_recommendation", methods=['GET'])
# def get_fertilizer_recommendation():
#     disease_name = request.args.get('disease')
#     fertilizer_recommendations = {
#         '_Late_blight': 'Copper-based fungicide',
#         '_Early_blight': 'Potassium bicarbonate',
#         'Spider_mites_Two_spotted_spider_mite': 'Insecticidal soap or neem oil',
#         '__Target_Spot': 'Copper fungicide',
#         '_Bacterial_spot': 'Copper-based fungicide or bactericide',
#         '_mosaic_viruss': 'No specific fertilizer; focus on removing infected plants and controlling vectors',
#         '_YellowLeaf__Curl_Virus': 'Nitrogen-rich fertilizer',
#         # Add more recommendations as needed
#     }
#     recommendation = fertilizer_recommendations.get(disease_name, None)
#     return jsonify({'recommendation': recommendation})


# if __name__ == "__main__":
#     app.run(debug=True)
