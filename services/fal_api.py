import os
import requests
from PIL import Image
import io
import base64
import json

FAL_API_KEY = os.getenv('FAL_API_KEY')
FAL_API_BASE_URL = 'https://fal.run'  # Standard fal.ai API endpoint

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

    # Handle image-to-image models
    if model['type'] == 'image-to-image' and image_file:
        # Convert image to base64
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        payload['image'] = img_str

    try:
        print(f"Sending request to: {FAL_API_BASE_URL}/{model['endpoint']}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f'{FAL_API_BASE_URL}/{model["endpoint"]}',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        # Direct return of the URL from the API response
        if 'images' in result and len(result['images']) > 0 and 'url' in result['images'][0]:
            return {'image_url': result['images'][0]['url']}
        
        print("Unexpected response structure:", result)
        raise Exception('No image URL in response')

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        raise Exception(f'API request failed: {str(e)}')
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise Exception(f'Failed to parse API response: {str(e)}')
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise 