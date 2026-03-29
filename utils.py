from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

def get_current_user(user_id: int = Cookie(None), role: str = Cookie(None), db: Session = Depends(get_db)):
    if not user_id or not role:
        raise HTTPException(401, "Not logged in")

    user = db.execute(text("SELECT * FROM Users WHERE id=:id"), {"id": user_id}).fetchone()

    if not user:
        raise HTTPException(401, "Invalid user")

    return user