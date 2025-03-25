# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


# Policy EIGHT tests
def test_check_password_policy_eight_valid(client):
    """
    Test a valid password for Policy EIGHT.
    """
    # Assuming AUTHOR starts with A-L for Policy EIGHT
    with app.app_context():
        # Setting AUTHOR within the test context
        app.config['AUTHOR'] = "aliced@seas.upenn.edu"
    resp = client.post("/v1/checkPassword", json={"password": "Password123!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is True
    assert "Policy EIGHT" in data.get("reason")


def test_check_password_policy_eight_too_short(client):
    """
    Test a password that is too short for Policy EIGHT.
    """
    with app.app_context():
        app.config['AUTHOR'] = "aliced@seas.upenn.edu"
    resp = client.post("/v1/checkPassword", json={"password": "Short!"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("valid") is False
    assert "too short" in data.get("reason")


def test_check_password_policy_eight_no_uppercase(client):
    """
    Test a password missing an uppercase letter for Policy EIGHT.
    """
    with app.app_context():
        app.config['AUTHOR'] = "aliced@seas.upenn.edu"
    resp = client.post("/v1/checkPassword", json={"password": "password123!"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("valid") is False
    assert "uppercase" in data.get("reason")


def test_check_password_policy_eight_no_digit(client):
    """
    Test a password missing a digit for Policy EIGHT.
    """
    with app.app_context():
        app.config['AUTHOR'] = "aliced@seas.upenn.edu"
    resp = client.post("/v1/checkPassword", json={"password": "Password!"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("valid") is False
    assert "digit" in data.get("reason")


def test_check_password_policy_eight_no_special_char(client):
    """
    Test a password missing a special character for Policy EIGHT.
    """
    with app.app_context():
        app.config['AUTHOR'] = "aliced@seas.upenn.edu"
    resp = client.post("/v1/checkPassword", json={"password": "Password123"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("valid") is False
    assert "special character" in data.get("reason")
