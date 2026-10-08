import os
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db


def get_current_user_id(
    db: Session = Depends(get_db),
) -> uuid.UUID:

    app_env = os.getenv(
        "APP_ENV",
        "development",
    )

    if app_env != "development":
        raise RuntimeError(
            "Development user authentication is disabled "
            "outside development mode."
        )

    email = os.getenv(
        "DEV_USER_EMAIL",
        "dev@example.com",
    )

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        user = User(
            email=email,
            name="Development User",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return user.id