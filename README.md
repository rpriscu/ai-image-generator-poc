# AI Image Generator

A Flask-based web application that generates AI images using fal.ai's API. The application features a modern dark-themed UI and supports multiple AI models for text-to-image generation.

![Zemingo Advanced Image Generator](static/images/screenshot.png)

## Features

- Clean, modern dark UI with Rubik font
- Text-to-image generation with 4 unique outputs per prompt
- Support for multiple fal.ai models:
  - FLUX.1 [dev] (default)
  - Recraft V3
  - Stable Diffusion V3
- Image download functionality
- Loading effects with image placeholders
- Responsive design for various screen sizes

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
2. Select an AI model (FLUX.1 is selected by default)
3. Click "Generate" button
4. Four different images will be generated based on your prompt
5. Hover over an image to reveal the download button
6. Click the download button to save the image to your device

## Project Structure

```
ai-image-generator-poc/
├── app.py                     # Main Flask application
├── templates/
│   └── index.html             # Frontend UI template
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling
│   └── images/
│       └── ZemingoLogo.png    # App logo
├── services/
│   └── fal_api.py             # fal.ai API interactions
├── .env                       # Environment variables
└── requirements.txt           # Project dependencies
```

## Recent Updates

- Added modern dark UI with Zemingo branding
- Implemented 2x2 image grid layout
- Added image download functionality
- Added animated loading placeholder effects
- Set FLUX.1 as the default model
- Removed untested models for stability

## License

MIT 