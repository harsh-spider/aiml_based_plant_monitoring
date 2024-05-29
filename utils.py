# import numpy as np
# import cv2
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array

# default_image_size = tuple((256, 256))

# def convert_image_to_array(image_dir):
#     try:
#         image = cv2.imread(image_dir)
#         if image is not None:
#             image = cv2.resize(image, default_image_size)
#             return img_to_array(image)
#         else:
#             return np.array([])
#     except Exception as e:
#         print(f"Error : {e}")
#         return None

# def load_trained_model(model_path):
#     model = load_model(model_path)
#     return model

# def prepare_image(image_dir):
#     image = convert_image_to_array(image_dir)
#     np_image = np.array(image, dtype=np.float16) / 225.0
#     np_image = np.expand_dims(np_image, axis=0)
#     return np_image


import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

default_image_size = (256, 256)

def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_frame_to_array(frame):
    try:
        image = cv2.resize(frame, default_image_size)
        return img_to_array(image)
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_trained_model(model_path):
    return load_model(model_path)

def prepare_image(image_dir):
    image = convert_image_to_array(image_dir)
    np_image = np.array(image, dtype=np.float16) / 255.0
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

def prepare_frame(frame):
    image = convert_frame_to_array(frame)
    np_image = np.array(image, dtype=np.float16) / 255.0
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


def detect_leaf(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        leaf_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(leaf_contour)
        min_leaf_area = 3000
        if area > min_leaf_area:
            return True
    return False