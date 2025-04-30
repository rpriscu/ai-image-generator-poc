# AI Image Generator

A Flask-based web application that generates images using fal.ai's API. The application supports multiple AI models for both text-to-image and image-to-image generation.

## Features

- Text-to-image generation
- Image-to-image generation (with reference image upload)
- Support for multiple fal.ai models:
  - FLUX.1 [dev]
  - Recraft V3
  - Stable Diffusion V3
  - Kolors Image-to-Image

## Prerequisites

- Python 3.11+
- fal.ai API key

## Setup

1. Clone the repository:
```bash
git clone git@github.com:rpriscu/ai-image-generator-poc.git
cd ai-image-generator-poc
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your fal.ai API key:
```
FAL_API_KEY=your_fal_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8080`

## Usage

1. Enter a text prompt describing the image you want to generate
2. Select an AI model from the dropdown
3. For image-to-image models, upload a reference image (optional)
4. Click "Generate Image" and wait for the result

## Project Structure

```
ai-image-generator-poc/
├── app.py                     # Main Flask application
├── templates/
│   └── index.html            # Frontend UI
├── services/
│   └── fal_api.py            # fal.ai API interactions
├── .env                      # Environment variables
└── requirements.txt          # Project dependencies
```

## License

MIT 