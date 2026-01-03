from app.models.user import User
from app.api.v1 import users as users_router


def create_user(db, email="test@example.com"):
    user = User(email=email, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def override_user(user):
    def _override():
        return user
    return _override
