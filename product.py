from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from utils import get_current_user

router = APIRouter(prefix="/product", tags=["Product"])

# ---------------- ADD PRODUCT ----------------
@router.post("/add-product")
def add_product(name: str, buying_price: float, selling_price: float,
                quantity: int, qty_alert: int,
                user=Depends(get_current_user),
                db: Session = Depends(get_db)):

    if user.role != "owner":
        raise HTTPException(403, "Only owner allowed")

    db.execute(text("""
        INSERT INTO Products (name, buying_price, selling_price, quantity, qty_alert)
        VALUES (:n,:b,:s,:q,:a)
    """), {"n": name, "b": buying_price, "s": selling_price, "q": quantity, "a": qty_alert})

    db.commit()
    return {"message": "Product added successfully"}


# ---------------- GET PRODUCT ----------------
@router.get("/get-product/{id}")
def get_product(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):

    product = db.execute(text("SELECT * FROM Products WHERE id=:id"), {"id": id}).fetchone()

    if not product:
        raise HTTPException(404, "Product not found")

    return dict(product._mapping)


# ---------------- UPDATE PRODUCT ----------------
@router.put("/update-product/{product_id}")
def update_product(product_id: int,
                   name: str = None,
                   buying_price: float = None,
                   selling_price: float = None,
                   quantity: int = None,
                   qty_alert: int = None,
                   user=Depends(get_current_user),
                   db: Session = Depends(get_db)):

    if user.role != "owner":
        raise HTTPException(403, "Only owner allowed")

    db.execute(text("""
        UPDATE Products
        SET 
            name = COALESCE(:name, name),
            buying_price = COALESCE(:buying_price, buying_price),
            selling_price = COALESCE(:selling_price, selling_price),
            quantity = COALESCE(:quantity, quantity),
            qty_alert = COALESCE(:qty_alert, qty_alert)
        WHERE id = :id
    """), {
        "name": name,
        "buying_price": buying_price,
        "selling_price": selling_price,
        "quantity": quantity,
        "qty_alert": qty_alert,
        "id": product_id
    })

    db.commit()
    return {"message": "Product updated"}


# ---------------- DELETE PRODUCT ----------------
@router.delete("/delete-product/{product_id}")
def delete_product(product_id: int,
                   user=Depends(get_current_user),
                   db: Session = Depends(get_db)):

    if user.role != "owner":
        raise HTTPException(403, "Only owner allowed")

    result = db.execute(text("DELETE FROM Products WHERE id=:id"), {"id": product_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(404, "Product not found")

    return {"message": "Product deleted"}