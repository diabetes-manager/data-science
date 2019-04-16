"""Entry point for Diabetes Manager flask application."""

# Since we're inside the app, we can
# use .app
from .app import create_app

APP = create_app()
