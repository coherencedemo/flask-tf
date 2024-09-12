import os
import logging
from flask import Flask
from google.cloud import storage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    logger.info('Received request for hello world')
    bucket_name = os.environ.get('BUCKET_NAME')
    logger.info(f'BUCKET_NAME environment variable: {bucket_name}')
    
    # Log all environment variables
    logger.info('All environment variables:')
    for key, value in os.environ.items():
        logger.info(f'{key}: {value}')
    
    return f'Hello, World! Your bucket name is: {bucket_name}'

@app.route('/list-files')
def list_files():
    logger.info('Received request to list files')
    bucket_name = os.environ.get('BUCKET_NAME')
    logger.info(f'Attempting to list files in bucket: {bucket_name}')
    
    if not bucket_name:
        logger.error('BUCKET_NAME environment variable is not set')
        return 'Error: BUCKET_NAME is not set', 500

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        files = bucket.list_blobs()
        file_list = ', '.join(f.name for f in files)
        logger.info(f'Successfully listed files: {file_list}')
        return file_list
    except Exception as e:
        logger.error(f'Error listing files: {str(e)}')
        return f'Error listing files: {str(e)}', 500

@app.route('/health')
def health_check():
    logger.info('Received health check request')
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f'Starting app on port {port}')
    logger.info('Initial environment variables:')
    for key, value in os.environ.items():
        logger.info(f'{key}: {value}')
    app.run(host='0.0.0.0', port=port)