"""Main application and logic for Diabetes Monitor"""
import pickle
from os import environ
import pandas as pd
from pathlib import Path

import psycopg2
from flask import Flask, jsonify, request

from .config import Config
from .dummy_data import load_so_cgm
from .models import DB
from .predict import make_prediction

DATA_DIR = Path(__file__).parents[1] / 'data'
MODEL_DIR = Path(__file__).parent / 'ml_models'

# load models
MODELS = []
for model_path in MODEL_DIR.iterdir():
    if str(model_path).endswith('.pkl'):
        with open(model_path, 'rb') as f:
            MODELS.append(pickle.load(f))


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
        return "This is a test"
        # return jsonify(message='Nothing here')

    @app.route('/predict', methods=['GET'])
    def predict():
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(
                message="Error: must pass user_id, e.g. /predict?user_id=1")

        # load user data
        if environ['FLASK_ENV'] == 'production':
            cur = DB.cursor()
            cur.execute(f"""
                SELECT (timestamp, value, below_threshold)
                FROM bloodsugar
                WHERE user_id = {user_id}
                LIMIT 3
            """)
            df = pd.DataFrame(
                cur.fetchall(),
                columns=['timestamp', 'value', 'below_threshold'])
        else:
            df = load_so_cgm()
            df = df.iloc[-10:]

        try:
            predictions = []
            for i, model in enumerate(MODELS):
                minutes = (i + 1) * 5
                predictions.append(make_prediction(df.copy(), model, minutes))
            df = pd.concat(predictions)
        except Exception as e:
            if environ['FLASK_ENV'] == 'production':
                return jsonify(message=f"Error: {e}")
            else:
                raise
        else:
            return jsonify(
                message="success",
                user_id=int(user_id),
                records=df.to_dict('records'),
            )

    @app.route('/build', methods=['GET'])
    def build():
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(
                message="Must pass user_id, e.g. /predict?user_id=1")

        return jsonify(message="success")

    return app
