import pickle, requests
from flask import Blueprint, request, jsonify

bp = Blueprint('utils', __name__)

# Insecure deserialization endpoint
@bp.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.get_data()
    obj = pickle.loads(data)   # unsafe
    return jsonify({"type": str(type(obj))})

# SSRF-like helper: fetch arbitrary URL (no validation)
@bp.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url')
    r = requests.get(url)   # no allow list -> SSRF demo
    return (r.text, r.status_code)

