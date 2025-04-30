# PythonAnywhere Deployment Guide

This guide provides step-by-step instructions for deploying the AI Image Generator on PythonAnywhere.

## Step 1: Set up a new Web App

1. Log in to your PythonAnywhere account
2. Click on the "Web" tab
3. Click "Add a new web app"
4. Choose your domain name (e.g., yourusername.pythonanywhere.com)
5. Select "Manual configuration"
6. Choose Python 3.8 or 3.9 (avoid 3.10+ to prevent compatibility issues)
7. Click "Next"

## Step 2: Clone the GitHub Repository

1. Go to the "Consoles" tab
2. Click "New console" → "Bash"
3. In the Bash console, run:

```bash
# Navigate to your home directory
cd ~

# Clone the repository
git clone https://github.com/rpriscu/ai-image-generator-poc.git

# Navigate to the project directory
cd ai-image-generator-poc

# Ensure requirements.txt has compatible versions
cat requirements.txt
```

## Step 3: Create a Virtual Environment

```bash
# Create a virtual environment with Python 3.8 or 3.9
mkvirtualenv --python=python3.9 ai-image-generator-env

# If the above command fails, try this instead:
python3 -m venv ~/ai-image-generator-env

# Activate the environment (if using venv)
source ~/ai-image-generator-env/bin/activate

# Install dependencies
pip install --no-binary :all: -r requirements.txt
```

## Step 4: Configure Environment Variables

```bash
# Create a .env file
echo "FAL_API_KEY=your_fal_api_key_here" > .env
```

Replace `your_fal_api_key_here` with your actual FAL API key.

## Step 5: Configure the Web App

1. Go back to the "Web" tab
2. Scroll down to the "Code" section
3. Set "Source code" to: `/home/yourusername/ai-image-generator-poc`
4. Set "Working directory" to: `/home/yourusername/ai-image-generator-poc`
5. Click on the WSGI configuration file link

Replace the contents of the WSGI file with:

```python
import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
path = '/home/yourusername/ai-image-generator-poc'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables from .env file
dotenv_path = os.path.join(path, '.env')
load_dotenv(dotenv_path)

# Import your Flask app
from app import app as application
```

Replace `yourusername` with your PythonAnywhere username.

## Step 6: Configure Virtual Environment Path

1. In the "Web" tab, under "Virtualenv", enter:
   - If using virtualenvwrapper: `/home/yourusername/.virtualenvs/ai-image-generator-env`
   - If using venv: `/home/yourusername/ai-image-generator-env`

## Step 7: Configure Static Files

In the "Static files" section, add:
- URL: `/static/` → Directory: `/home/yourusername/ai-image-generator-poc/static`

## Step 8: Reload the Web App

Click the green "Reload" button at the top of the page.

## Troubleshooting

If you encounter issues:

1. Check the error logs in the "Web" tab → "Error log"
2. Make sure your virtual environment has all dependencies installed correctly
3. Verify the paths in the WSGI file match your actual directory structure
4. Try a different Python version (3.8 may work better than 3.9 in some cases)
5. If you see errors related to wheel or compilation, try this alternative approach:

```bash
# Go back to your bash console
cd ~/ai-image-generator-poc

# Activate your virtual environment
source ~/ai-image-generator-env/bin/activate

# Install packages without building wheels
pip install --no-cache-dir Flask==3.0.2
pip install --no-cache-dir python-dotenv==1.0.1
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir Pillow==9.5.0
```

After making any changes, reload your web app from the "Web" tab. 