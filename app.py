import os
import logging
from flask import Flask
from google.cloud import storage

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def hello_world():
    app.logger.info('Received request for hello world')
    bucket_name = os.environ.get('BUCKET_NAME')
    app.logger.info(f'BUCKET_NAME environment variable: {bucket_name}')
    app.logger.info(f'All environment variables: {dict(os.environ)}')
    return f'Hello, World! Your bucket name is: {bucket_name}'

@app.route('/list-files')
def list_files():
    bucket_name = os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    files = bucket.list_blobs()
    return ', '.join(f.name for f in files)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.logger.info(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port)