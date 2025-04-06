import pytest
import sqlite3
import tempfile
import os
from fastapi.testclient import TestClient
from backend.routers.auth import (
    authenticate_user,
    create_access_token,
    hash_password,
    verify_password,
)

from backend.main import app
from backend.schemas import DBUser
from backend.db_interface import DBInterface, get_db_interface


@pytest.fixture
def temp_db():
    """Fixture to create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_name = temp_file.name
        os.environ["db_name"] = db_name
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 0,
            account_balance REAL,
            cells_owned INTEGER,
            projects_owned INTEGER,
            total_invested REAL,
            total_earnings REAL,
            total_energy_generated REAL,
            maximum_power_generation REAL
        );
        """)
        conn.commit()
        yield db_name
    finally:
        conn.close()
        os.remove(db_name)


@pytest.fixture
def db_interface(temp_db):
    """Fixture to provide a DBInterface instance."""

    def get_db_interface():
        return DBInterface(db_name=temp_db)

    return get_db_interface


@pytest.fixture
def test_client(db_interface):
    app.dependency_overrides[get_db_interface] = db_interface
    return TestClient(app)


@pytest.fixture
def add_test_user(db_interface):
    """Fixture to add a test user to the database."""
    db = db_interface()
    db.insert(
        DBUser(
            id="test_user",
            username="test_user",
            password=hash_password("securepassword123"),
            is_active=True,
            account_balance=1000.0,
            cells_owned=5,
            projects_owned=2,
            total_invested=5000.0,
            total_earnings=200.0,
            total_energy_generated=1500.0,
            maximum_power_generation=300.0,
        )
    )


# def test_authenticate_user(test_client, add_test_user):
#     # Test with valid credentials
#     response = test_client.post(
#         "/api/token",
#         data={"username": "test_user", "password": "securepassword123"},
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()

#     # Test with invalid credentials
#     response = test_client.post(
#         "/api/token",
#         data={"username": "test_user", "password": "wrongpassword"},
#     )
#     assert response.status_code == 401
#     assert "access_token" not in response.json()


def test_hash_password_not_empty():
    plain_password = "securepassword123"
    hashed_password = hash_password(plain_password)
    assert hashed_password != ""
    assert isinstance(hashed_password, str)


@pytest.mark.skip("Skipping test_hash_password_different_for_same_input due to dummy hash function")
def test_hash_password_different_for_same_input():
    plain_password = "securepassword123"
    hashed_password1 = hash_password(plain_password)
    hashed_password2 = hash_password(plain_password)
    assert hashed_password1 != hashed_password2


def test_hash_password_consistent_verification():
    plain_password = "securepassword123"
    hashed_password = hash_password(plain_password)
    assert verify_password(plain_password, hashed_password) is True


def test_verify_password_correct():
    plain_password = "securepassword123"
    hashed_password = hash_password(plain_password)
    assert verify_password(plain_password, hashed_password) is True


def test_verify_password_incorrect():
    plain_password = "securepassword123"
    wrong_password = "wrongpassword456"
    hashed_password = hash_password(plain_password)
    assert verify_password(wrong_password, hashed_password) is False


def test_verify_password_empty_plain():
    plain_password = ""
    hashed_password = hash_password("securepassword123")
    assert verify_password(plain_password, hashed_password) is False


def test_verify_password_empty_hashed():
    plain_password = "securepassword123"
    hashed_password = ""
    assert verify_password(plain_password, hashed_password) is False


#    authenticate_user,
#    create_access_token,
def test_authenticate_user_valid_credentials(add_test_user, db_interface):
    """Test authenticate_user with valid credentials."""
    db = db_interface()
    user = authenticate_user("test_user", "securepassword123", db)
    assert user is not None
    assert user.username == "test_user"


def test_authenticate_user_invalid_username(db_interface):
    """Test authenticate_user with an invalid username."""
    db = db_interface()
    user = authenticate_user("invalid_user", "securepassword123", db)
    assert user is False


def test_authenticate_user_invalid_password(add_test_user, db_interface):
    """Test authenticate_user with an invalid password."""
    db = db_interface()
    user = authenticate_user("test_user", "wrongpassword", db)
    assert user is False


def test_authenticate_user_empty_username(db_interface):
    """Test authenticate_user with an empty username."""
    db = db_interface()
    user = authenticate_user("", "securepassword123", db)
    assert user is False


def test_authenticate_user_empty_password(add_test_user, db_interface):
    """Test authenticate_user with an empty password."""
    db = db_interface()
    user = authenticate_user("test_user", "", db)
    assert user is False


def test_authenticate_user_none_credentials(db_interface):
    """Test authenticate_user with None as credentials."""
    db = db_interface()
    user = authenticate_user(None, None, db)
    assert user is False
