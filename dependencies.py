from fastapi import Depends, HTTPException, status

from oauth2 import get_current_user
from models import User


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can perform this action."
        )
    return current_user


def manager_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Store Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
    return current_user