from flask import Flask, request, jsonify, render_template_string
from google.cloud import storage
import os

app = Flask(__name__)

# Use the CNC_INSTANCE_NAME to derive the bucket name
BUCKET_NAME = f"bucket-{os.environ['CNC_INSTANCE_NAME']}"

@app.route('/')
def index():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    files = [blob.name for blob in blobs]
    
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
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        return jsonify({"message": f"File {file.filename} uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))