from flask import Flask, render_template_string
from google.cloud import storage
import os
import logging
import sys

app = Flask(__name__)

# Configure logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the bucket name from environment variable
BUCKET_NAME = os.environ.get('CUSTOM_BUCKET_NAME')
logger.info(f"BUCKET_NAME: {BUCKET_NAME}")

def list_files(bucket_name):
    logger.debug(f"Attempting to list files from bucket: {bucket_name}")
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        
        files = []
        for blob in blobs:
            logger.debug(f"Processing blob: {blob.name}, Content-Type: {blob.content_type}")
            public_url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
            files.append({'name': blob.name, 'url': public_url})
        
        logger.info(f"Successfully listed {len(files)} files")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise

@app.route('/')
def index():
    logger.debug("Entering index route")
    try:
        files = list_files(BUCKET_NAME)
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>File Gallery</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                    h1 { color: #333; }
                    .gallery { display: flex; flex-wrap: wrap; gap: 20px; }
                    .file-container { width: 300px; }
                    img { max-width: 100%; height: auto; }
                </style>
            </head>
            <body>
                <h1>File Gallery</h1>
                <div class="gallery">
                    {% for file in files %}
                        <div class="file-container">
                            {% if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) %}
                                <img src="{{ file.url }}" alt="{{ file.name }}">
                            {% endif %}
                            <p>{{ file.name }}</p>
                        </div>
                    {% endfor %}
                </div>
            </body>
            </html>
        ''', files=files)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return str(e), 500

@app.route('/debug')
def debug():
    logger.debug("Entering debug route")
    try:
        storage_client = storage.Client()
        return {
            "BUCKET_NAME": BUCKET_NAME,
            "project": storage_client.project,
            "credentials_type": type(storage_client.credentials).__name__,
            "ENV_VARS": dict(os.environ)
        }
    except Exception as e:
        logger.error(f"Error in debug route: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)