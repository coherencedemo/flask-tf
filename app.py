import os
import logging
from flask import Flask

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def hello_world():
    app.logger.info('Received request for hello world')
    return 'Hello, World!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.logger.info(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port)