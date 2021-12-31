import pytest
import flaskapp

@pytest.fixture
def client():
    # Prepare before your test
    flaskapp.app.config["TESTING"] = True
    with flaskapp.app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example