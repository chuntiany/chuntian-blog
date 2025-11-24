import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app import create_app
from extensions import db
from models import User

@pytest.fixture
def app():
    # Use a separate test database or in-memory sqlite for testing?
    # For now, let's use the same DB but maybe with a different config?
    # Or just mock?
    # Let's use SQLite in-memory for tests to avoid messing with real DB
    class TestConfig:
        SECRET_KEY = 'test_key'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TESTING = True

    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
