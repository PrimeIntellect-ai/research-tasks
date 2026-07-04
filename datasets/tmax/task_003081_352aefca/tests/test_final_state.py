# Vulnerable Example
import os
from flask import Flask, request, send_file

app = Flask(__name__)
BASE_DIR = "/app/public_files/"

@app.route('/download')
def download():
    filename = request.args.get('file')
    # Vulnerable: No validation on 'filename'
    filepath = os.path.join(BASE_DIR, filename) 
    return send_file(filepath)