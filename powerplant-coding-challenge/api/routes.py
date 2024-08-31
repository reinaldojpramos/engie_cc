from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/')
def home():
    return jsonify(message="Powerplant Coding Challenge")
