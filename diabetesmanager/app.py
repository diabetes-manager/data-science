"""Main application and logic for Diabetes Monitor"""
# from decouple import config
import pickle
from flask import Flask, request
from flask_json import json_response


def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    app.config['JSON_ADD_STATUS'] = False

    with open('diabetesmanager/data/private/table', 'rb') as f:
        table = pickle.load(f)

    def select_table_values(start_idx, length):
        len_to_return = length
        if start_idx > table.shape[0]:
            return 'Start index too large'
        elif start_idx + length > table.shape[0]:
            len_to_return = table.shape[0] - start_idx

        df = table.iloc[start_idx:start_idx + len_to_return, :]
        return df

    @app.route('/')
    def root():
        return json_response(data='Nothing here')

    @app.route('/data', methods=['GET'])
    def data():
        start_idx = request.args.get('start')
        length = request.args.get('length')

        selected_table = select_table_values(
            int(start_idx), int(length)).to_json(orient='records')

        return json_response(data=selected_table)

    return app
