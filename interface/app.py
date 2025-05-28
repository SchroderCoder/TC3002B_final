import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)

# Config
UPLOAD_FOLDER = 'interface/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
model = load_model('interface/beatles_recognizer.keras')

# Define your class labels (adjust if needed)
class_names = ['john', 'paul', 'george', 'ringo']

def predict_image(img_path):
    # Load and preprocess the image
    img = load_img(img_path, target_size=(224, 224), color_mode='grayscale')
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)[0]
    predicted_index = np.argmax(predictions)
    confidence = float(predictions[predicted_index]) * 100

    return class_names[predicted_index], confidence, predictions

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    filename = None
    all_probs = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            prediction, confidence, all_probs = predict_image(filepath)

    return render_template('index.html',
                           prediction=prediction,
                           confidence=confidence,
                           filename=filename,
                           all_probs=all_probs,
                           class_names=class_names)

if __name__ == '__main__':
    app.run(debug=True)
