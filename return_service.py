from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from utils import get_current_user

router = APIRouter(prefix="/return", tags=["Return"])


# ---------------- RETURN PRODUCT ----------------
@router.post("/return-product")
def return_product(product_id: int,
                   quantity: int,
                   user=Depends(get_current_user),
                   db: Session = Depends(get_db)):

    product = db.execute(text("SELECT * FROM Products WHERE id=:id"),
                         {"id": product_id}).fetchone()

    if not product:
        raise HTTPException(404, "Product not found")

    refund = product.selling_price * quantity

    # increase stock
    db.execute(text("""
        UPDATE Products SET quantity = quantity + :q WHERE id=:id
    """), {"q": quantity, "id": product_id})

    # insert return record
    db.execute(text("""
        INSERT INTO Returns (product_id, quantity, refund_amount)
        VALUES (:p,:q,:r)
    """), {"p": product_id, "q": quantity, "r": refund})

    db.commit()

    return {
        "message": "Product returned successfully",
        "refund": refund
    }


# ---------------- DAILY RETURNS ----------------
@router.get("/daily-returns")
def daily_returns(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT product_id, 
               SUM(quantity) as total_qty, 
               SUM(refund_amount) as total_returns
        FROM Returns
        WHERE CAST(created_at AS DATE) = CAST(GETDATE() AS DATE)
        GROUP BY product_id
    """)).fetchall()

    return [dict(row._mapping) for row in result]