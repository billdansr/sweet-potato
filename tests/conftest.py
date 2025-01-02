import pytest
from app import create_app  # Replace with your Flask app factory function
from db import init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:',  # Use in-memory SQLite database for testing
        'UPLOAD_DIR': '/tmp/uploads',  # Temporary directory for file uploads
    })

    with app.app_context():
        init_db()

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()
