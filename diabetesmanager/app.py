"""Main application and logic for Diabetes Monitor"""
import pickle
from pathlib import Path

from flask import Flask, request
from flask_json import json_response
import psycopg2

from .config import Config
from .models import DB
from .predict import make_prediction
from .dummy_data import load_so_cgm

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
        return json_response(data='Nothing here')

    @app.route('/data', methods=['GET'])
    def data():
        user_id = request.args.get('userid')
        start_idx = request.args.get('start')
        length = request.args.get('length')

        # load model
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        # TODO: query for user data here
        df = load_so_cgm()

        predictions = make_prediction(df, model)

        # TODO: return predictions
        predictions = predictions.to_json(orient='records')

        return json_response(data=predictions)

    return app
