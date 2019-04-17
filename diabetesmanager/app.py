"""Main application and logic for Diabetes Monitor"""
import pickle
from pathlib import Path

from flask import Flask, request
from flask_json import json_response

from .config import Config

DATA_DIR = Path(__file__).parents[1] / 'data'


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

    @app.route('/')
    def root():
        return json_response(data='Nothing here')

    @app.route('/data', methods=['GET'])
    def data():
        start_idx = request.args.get('start')
        length = request.args.get('length')

        # TODO: write model to and read model from production database
        with open(DATA_DIR / 'private' / 'table', 'rb') as f:
            table = pickle.load(f)

        selected_table = select_table_values(
            table, int(start_idx), int(length)
        ).to_json(orient='records')

        return json_response(data=selected_table)

    return app
