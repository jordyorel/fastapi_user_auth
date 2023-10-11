from app.models.user import User

def test_create_user():
    # Create a user
    user = User(email="user@mail.com", password="password", role=1, is_active=True)
    assert user.email == "user@mail.com"
    assert user.role == 1
    assert user.is_active == True
    assert user.password == "password"