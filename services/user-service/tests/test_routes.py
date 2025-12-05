import pytest
from crud import create_user, confirm_user, get_user_by_email, create_recovery_code, reset_password


def test_user_registration(test_client, test_db):
    """Test user registration endpoint"""
    response = test_client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify user was created
    user = get_user_by_email(test_db, "test@example.com")
    assert user is not None
    assert user.name == "Test User"
    assert user.confirmed is False


def test_email_confirmation(test_client, test_db):
    """Test email confirmation endpoint"""
    # Create a user
    create_user(test_db, "Test User", "test@example.com", "password123")
    user = get_user_by_email(test_db, "test@example.com")
    code = user.confirmation_code
    
    # Confirm email
    response = test_client.post(
        "/users/confirm",
        json={
            "email": "test@example.com",
            "code": code
        }
    )
    assert response.status_code == 200
    
    # Verify user is confirmed
    user = get_user_by_email(test_db, "test@example.com")
    assert user.confirmed is True


def test_user_login_success(test_client, test_db):
    """Test successful user login"""
    # Create and confirm a user
    create_user(test_db, "Test User", "test@example.com", "password123")
    user = get_user_by_email(test_db, "test@example.com")
    confirm_user(test_db, "test@example.com", user.confirmation_code)
    
    # Login
    response = test_client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_user_login_invalid_credentials(test_client, test_db):
    """Test login with invalid credentials"""
    # Create and confirm a user
    create_user(test_db, "Test User", "test@example.com", "password123")
    user = get_user_by_email(test_db, "test@example.com")
    confirm_user(test_db, "test@example.com", user.confirmation_code)
    
    # Try to login with wrong password
    response = test_client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_user_login_unconfirmed(test_client, test_db):
    """Test login with unconfirmed email"""
    # Create a user but don't confirm
    create_user(test_db, "Test User", "test@example.com", "password123")
    
    # Try to login
    response = test_client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 403


def test_password_recovery(test_client, test_db):
    """Test password recovery flow"""
    # Create and confirm a user
    create_user(test_db, "Test User", "test@example.com", "password123")
    user = get_user_by_email(test_db, "test@example.com")
    confirm_user(test_db, "test@example.com", user.confirmation_code)
    
    # Request password recovery
    response = test_client.post(
        "/users/recover",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    
    # Get recovery code
    user = get_user_by_email(test_db, "test@example.com")
    code = user.recovery_code
    
    # Reset password
    response = test_client.post(
        "/users/reset",
        json={
            "email": "test@example.com",
            "code": code,
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 200
    
    # Try to login with new password
    response = test_client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 200


def test_duplicate_email_registration(test_client, test_db):
    """Test that duplicate email registration is rejected"""
    # Create first user
    response = test_client.post(
        "/users/register",
        json={
            "name": "Test User 1",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    
    # Try to create another user with same email
    response = test_client.post(
        "/users/register",
        json={
            "name": "Test User 2",
            "email": "test@example.com",
            "password": "password456"
        }
    )
    assert response.status_code == 400
