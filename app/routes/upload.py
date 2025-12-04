import os
from flask import Blueprint, request, jsonify, send_from_directory

bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Insecure file upload: no validation, no restriction
@bp.route('/file', methods=['POST'])
def file_upload():
    f = request.files.get('file')
    if not f:
        return jsonify({"error":"no file"}), 400
    # vulnerable: allow filename as provided -> directory traversal
    filename = f.filename
    target = os.path.join(UPLOAD_FOLDER, filename)
    f.save(target)
    return jsonify({"saved": filename}), 201

@bp.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    # serve files directly from uploads -> potential sensitive file leak
    return send_from_directory(UPLOAD_FOLDER, filename)

