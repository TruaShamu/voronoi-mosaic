from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import json
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from scipy.spatial import Voronoi
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    json_file_path = os.path.join(app.root_path, 'static', 'image_data.json')

    try:
        with open(json_file_path, 'r') as file:
            image_data = json.load(file)
    except FileNotFoundError:
        image_data = []
    return render_template('index.html', images=image_data)

class VoronoiMosaic:
    @staticmethod
    def generate_seeds(image_shape, num_seeds):
        """Generate random seeds for the Voronoi diagram."""
        h, w = image_shape[:2]
        seeds = np.column_stack((
            np.random.randint(0, w, num_seeds),
            np.random.randint(0, h, num_seeds)
        ))
        return seeds

    @staticmethod
    def region_color(image, vor, seeds):
        """Assign colors to Voronoi regions based on the input image."""
        region_colors = np.zeros((len(seeds), 3), dtype=np.uint8)
        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            if region and -1 not in region:  # Valid region
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                polygon = np.array([vor.vertices[vertex] for vertex in region], dtype=np.int32)
                cv2.fillPoly(mask, [polygon], 1)
                if np.any(mask):
                    region_colors[i] = np.mean(image[mask.astype(bool)], axis=0)
        return region_colors

    @staticmethod
    def generate_mosaic(image, num_seeds):
        """Generate a Voronoi mosaic for the given image."""
        seeds = VoronoiMosaic.generate_seeds(image.shape, num_seeds)
        vor = Voronoi(seeds)
        region_colors = VoronoiMosaic.region_color(image, vor, seeds)
        output_image = np.zeros_like(image)

        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            if region and -1 not in region:
                polygon = np.array([vor.vertices[vertex] for vertex in region], dtype=np.int32)
                cv2.fillPoly(output_image, [polygon], region_colors[i].tolist())

        return output_image


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['image']
        if not file:
            return jsonify({'error': 'No selected file'}), 400

        # Read the image file into memory
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image file'}), 400

        try:
            num_seeds = int(request.form['seeds'])
            output_image = VoronoiMosaic.generate_mosaic(image, num_seeds)
            
            is_success, buffer = cv2.imencode('.png', output_image)
            if not is_success:
                return jsonify({'error': 'Failed to encode output image'}), 500
            
            encoded_image = base64.b64encode(buffer.tobytes()).decode('utf-8')
            
            return jsonify({
                'mosaic_image': encoded_image
            })
            
        except ValueError:
            return jsonify({'error': 'Invalid number of seeds'}), 400
        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500

    return render_template('generate.html')

if __name__ == '__main__':
    app.run(debug=True)