from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from utils import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/billing", tags=["Billing"])

class Item(BaseModel):
    product_id: int
    quantity: int


# ---------------- CREATE BILL ----------------
@router.post("/create-bill")
def create_bill(items: List[Item],
                user=Depends(get_current_user),
                db: Session = Depends(get_db)):

    if user.role != "seller":
        raise HTTPException(403, "Only seller allowed")

    bill_id = db.execute(text("SELECT ISNULL(MAX(bill_id),0)+1 FROM BillItems")).scalar()

    total = 0
    bill_items = []

    for item in items:
        product = db.execute(text("SELECT * FROM Products WHERE id=:id"),
                             {"id": item.product_id}).fetchone()

        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")

        if product.quantity < item.quantity:
            raise HTTPException(400, "Not enough stock")

        cost = product.selling_price * item.quantity
        total += cost

        # reduce stock
        db.execute(text("""
            UPDATE Products SET quantity = quantity - :q WHERE id=:id
        """), {"q": item.quantity, "id": item.product_id})

        # insert bill item
        db.execute(text("""
            INSERT INTO BillItems (bill_id, product_id, quantity, price)
            VALUES (:b,:p,:q,:price)
        """), {
            "b": bill_id,
            "p": item.product_id,
            "q": item.quantity,
            "price": cost
        })

        bill_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": cost
        })

    db.commit()

    return {
        "message": "Bill created successfully",
        "bill_id": bill_id,
        "total": total,
        "items": bill_items
    }


# ---------------- DAILY SALES ----------------
@router.get("/daily-sales")
def daily_sales(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT product_id, 
               SUM(quantity) as total_qty, 
               SUM(price) as total_sales
        FROM BillItems
        WHERE CAST(created_at AS DATE) = CAST(GETDATE() AS DATE)
        GROUP BY product_id
    """)).fetchall()

    return [dict(row._mapping) for row in result]