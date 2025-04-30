import os
import requests
from PIL import Image
import io
import base64
import json

FAL_API_KEY = os.getenv('FAL_API_KEY')
FAL_API_BASE_URL = 'https://fal.run'

def generate_image(prompt, model, image_file=None):
    """
    Generate an image using the specified fal.ai model.
    
    Args:
        prompt (str): The text prompt for image generation
        model (dict): The model configuration
        image_file (FileStorage, optional): The reference image file for image-to-image models
    
    Returns:
        dict: The generated image data
    """
    headers = {
        'Authorization': f'Key {FAL_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Base payload
    payload = {
        'prompt': prompt
    }

    # Add model-specific parameters if they exist
    if 'params' in model:
        payload.update(model['params'])

    # Handle image-to-image models
    if (model['type'] == 'image-to-image' or model['type'] == 'hybrid') and image_file:
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        payload['image_url'] = f"data:image/png;base64,{img_str}"

    try:
        print(f"Making request to: {FAL_API_BASE_URL}/{model['endpoint']}")
        print(f"With payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f'{FAL_API_BASE_URL}/{model["endpoint"]}',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if not response.ok:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
            except:
                pass
            raise Exception(error_msg)
            
        result = response.json()
        
        # Handle different response formats
        if 'images' in result and len(result['images']) > 0:
            if isinstance(result['images'][0], str):
                return {'image_url': result['images'][0]}
            elif isinstance(result['images'][0], dict) and 'url' in result['images'][0]:
                return {'image_url': result['images'][0]['url']}
        elif 'image' in result:
            if isinstance(result['image'], str):
                return {'image_url': result['image']}
            elif isinstance(result['image'], dict) and 'url' in result['image']:
                return {'image_url': result['image']['url']}
        
        print("Unexpected response structure:", result)
        raise Exception('No image URL found in response')

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        raise Exception(f'API request failed: {str(e)}')
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise Exception(f'Failed to parse API response: {str(e)}')
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise 