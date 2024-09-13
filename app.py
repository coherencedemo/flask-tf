from flask import Flask, render_template_string
from google.cloud import storage
import os

app = Flask(__name__)

# Get the bucket name from environment variable
BUCKET_NAME = os.environ.get('CUSTOM_BUCKET_NAME')

def list_files(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    
    files = []
    for blob in blobs:
        if blob.content_type.startswith('image/'):
            url = blob.generate_signed_url(expiration=3600)  # URL valid for 1 hour
            files.append({'name': blob.name, 'url': url})
    return files

@app.route('/')
def index():
    files = list_files(BUCKET_NAME)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Gallery</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                h1 { color: #333; }
                .gallery { display: flex; flex-wrap: wrap; gap: 20px; }
                .image-container { width: 300px; }
                img { max-width: 100%; height: auto; }
            </style>
        </head>
        <body>
            <h1>Image Gallery</h1>
            <div class="gallery">
                {% for file in files %}
                    <div class="image-container">
                        <img src="{{ file.url }}" alt="{{ file.name }}">
                        <p>{{ file.name }}</p>
                    </div>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))