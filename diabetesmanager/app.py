"""Main application and logic for Diabetes Monitor"""
import pickle
from pathlib import Path

import psycopg2
from flask import Flask, jsonify, request

from .config import Config
from .dummy_data import load_so_cgm
from .models import DB
from .predict import make_prediction

DATA_DIR = Path(__file__).parents[1] / 'data'
MODEL_PATH = Path(__file__).parent / 'model.pkl'


def select_table_values(table, start_idx, length):
    len_to_return = length
    if start_idx > table.shape[0]:
        return 'Start index too large'
    elif start_idx + length > table.shape[0]:
        len_to_return = table.shape[0] - start_idx

    df = table.iloc[start_idx:start_idx + len_to_return, :]

    return df


def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.shell_context_processor
    def make_shell_context():
        return {'DB': DB}

    @app.route('/')
    def root():
        return jsonify(message='Nothing here')

    @app.route('/predict', methods=['GET'])
    def predict():
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(
                message="Error: must pass user_id, e.g. /predict?user_id=1"
            )

        # load model
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        # TODO: query for filtered user_id data here
        df = load_so_cgm()

        df = make_prediction(df, model)

        # TODO: rather than return JSON, we could save predictions to DB
        response = jsonify(
            message="success",
            user_id=int(user_id),
            records=df.to_dict('records'),
        )

        return response

    @app.route('/build', methods=['GET'])
    def build():
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(
                message="Must pass user_id, e.g. /predict?user_id=1"
            )

        return jsonify(message="success")

    return app
