import pytest
import server

@pytest.fixture
def client():
    # Prepare before your test
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example