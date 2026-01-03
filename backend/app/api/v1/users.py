from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get(
    "/profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.put(
    "/profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete(
    "/profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db.delete(current_user)
    db.commit()

    return None

