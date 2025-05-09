from flask import Flask, render_template, request, redirect, url_for
from deepface import DeepFace
import os

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

upload_folder = 'static/uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

db_folder = 'static/db_images'
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Function to get all images from the 'db_images' folder
def get_all_images():
    image_list = []
    for filename in os.listdir(db_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(db_folder, filename)
            image_list.append((filename, image_path))
    
    return image_list

@app.route('/upload', methods=['POST'])
def upload_image():
    uploaded_file = request.files['image']
    
    if uploaded_file:
        uploaded_image_name = uploaded_file.filename
        uploaded_file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(uploaded_file_path)
        
        # Fetch images from the 'db_images' folder
        db_images = get_all_images() 
        
        matches = []
        for name, db_image_path in db_images:
            # Use DeepFace.verify to compare the uploaded image against the database image
            result = DeepFace.verify(img1_path=uploaded_file_path, img2_path=db_image_path, model_name='Facenet')
            
            if result['verified']:  # Check if the match is verified
                matches.append((name, result['distance']))  # Store matched image name and distance
                break  # Exit the loop if a match is found
            
        return render_template('results.html', matches=matches, uploaded_image=uploaded_image_name)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
