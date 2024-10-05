from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model (ensure you have the correct path to your model)
model = pickle.load(open("savedmodel.sav", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html') 

@app.route('/result', methods=['POST'])  # This route will handle the prediction
def result():
    if request.method == 'POST':
        # Collect the form data
        mean_radius = float(request.form['mean_radius'])
        mean_texture = float(request.form['mean_texture'])
        mean_perimeter = float(request.form['mean_perimeter'])
        mean_area = float(request.form['mean_area'])
        mean_smoothness = float(request.form['mean_smoothness'])
        
        # Combine inputs into an array
        inputs = np.array([[mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness]])
        
        # Use the loaded model to make predictions
        prediction = model.predict(inputs)
        
        # Interpret the result (assuming 1 = benign, 0 = malignant)
        if prediction[0] == 1:
            result_text = "The Breast Cancer is Benign"
        else:
            result_text = "The Breast Cancer is Malignant"
        
        # Render the result on a new page
        return render_template('result.html', prediction=result_text)
@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/about')
def about():
    return render_template('about.html') 

if __name__ == "__main__":
    app.run(debug=True)
