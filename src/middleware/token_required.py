# auth.py
from functools import wraps
from flask import request, jsonify
from src.utils.security import Security


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Security.verify_token(request.headers)
        if not data["success"]:
            return jsonify(data), status
        return f(*args, **kwargs)

    return decorated
