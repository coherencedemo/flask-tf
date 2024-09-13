from flask import Flask, request, jsonify, render_template_string
from google.cloud import storage
import os

app = Flask(__name__)

# Get the bucket name from environment variable
BUCKET_NAME = os.environ.get('BUCKET_NAME')

# Initialize GCS client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

@app.route('/')
def index():
    files = list_files()
    return render_template_string('''
        <h1>File Upload and List</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        <h2>Files in bucket:</h2>
        <ul>
            {% for file in files %}
                <li>{{ file }}</li>
            {% endfor %}
        </ul>
    ''', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        blob = bucket.blob(file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        return jsonify({"message": f"File {file.filename} uploaded successfully"}), 200

def list_files():
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))