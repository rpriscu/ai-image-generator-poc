from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from services.fal_api import generate_image

# Load environment variables
load_dotenv()

# Verify API key is loaded (temporary)
api_key = os.getenv('FAL_API_KEY')
print(f"API Key loaded: {'YES' if api_key else 'NO'}")

app = Flask(__name__)

# Configure maximum file size for uploads (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Available models configuration
AVAILABLE_MODELS = {
    'flux': {
        'name': 'FLUX.1 [dev]',
        'endpoint': 'fal-ai/flux',
        'type': 'text-to-image'
    },
    'recraft': {
        'name': 'Recraft V3',
        'endpoint': 'fal-ai/recraft-v3',
        'type': 'text-to-image',
        'params': {
            'style_name': 'vector-art'
        }
    },
    'stable_diffusion': {
        'name': 'Stable Diffusion V3',
        'endpoint': 'fal-ai/stable-diffusion-v3-medium',
        'type': 'text-to-image',
        'description': 'Creates detailed images with high fidelity.',
        'params': {
            'num_inference_steps': 30,
            'guidance_scale': 7.5
        }
    }
}

@app.route('/')
def index():
    return render_template('index.html', models=AVAILABLE_MODELS)

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.form
        prompt = data.get('prompt')
        model_id = data.get('model')
        image_file = request.files.get('image')
        num_images = int(data.get('num_images', 1))  # Default to 1 if not specified

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        if not model_id or model_id not in AVAILABLE_MODELS:
            return jsonify({'error': 'Invalid model selected'}), 400

        model = AVAILABLE_MODELS[model_id]
        
        # Limit number of images to generate
        num_images = min(num_images, 4)  # Maximum 4 images
        
        # Track generated images
        image_urls = []
        
        # Generate the requested number of images
        for _ in range(num_images):
            # Generate image using the selected model
            result = generate_image(
                prompt=prompt,
                model=model,
                image_file=image_file if model['type'] == 'image-to-image' else None
            )
            
            if 'image_url' in result:
                image_urls.append(result['image_url'])
        
        # If we couldn't generate any images, return an error
        if not image_urls:
            return jsonify({'error': 'Failed to generate any images'}), 500
            
        return jsonify({'image_urls': image_urls})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 