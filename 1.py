from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Set the working directory
os.chdir("/path/to/your/script_and_model_files")

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Function to process and predict image
def process_and_predict_text():
    # Get the original text from the textbox
    original_text = original_text_entry.get()

    # You can perform any necessary processing on the original text here
    # For example, if your model works with images, you might convert the text to an image.

    # Dummy process for illustration (replace with actual processing)
    processed_image_array = np.ones((224, 224, 3), dtype=np.float32)

    # Load the processed data into the array
    data[0] = processed_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    result_label.config(text=f"Class: {class_name[2:]} - Confidence Score: {confidence_score}")

# GUI setup
root = tk.Tk()
root.title("Text Prediction")

# Create a label and entry for the original text
original_text_label = tk.Label(root, text="Enter Original Text:")
original_text_label.pack()

original_text_entry = tk.Entry(root, width=50)
original_text_entry.pack()

# Create a button to trigger the prediction
predict_button = tk.Button(root, text="Predict Text", command=process_and_predict_text)
predict_button.pack()

# Create a label to display the prediction result
result_label = tk.Label(root, text="")
result_label.pack()

# Run the GUI
root.mainloop()
