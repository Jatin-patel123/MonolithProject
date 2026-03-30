from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/report", tags=["Report"])


@router.get("/daily-report")
def daily_report(db: Session = Depends(get_db)):

    sales = db.execute(text("""
        SELECT product_id, SUM(quantity) as total_qty, SUM(price) as total_sales
        FROM BillItems
        WHERE CAST(created_at AS DATE) = CAST(GETDATE() AS DATE)
        GROUP BY product_id
    """)).fetchall()

    returns = db.execute(text("""
        SELECT product_id, SUM(quantity) as total_qty, SUM(refund_amount) as total_returns
        FROM Returns
        WHERE CAST(created_at AS DATE) = CAST(GETDATE() AS DATE)
        GROUP BY product_id
    """)).fetchall()

    sales_dict = {row.product_id: row for row in sales}
    returns_dict = {row.product_id: row for row in returns}

    all_products = set(sales_dict.keys()) | set(returns_dict.keys())

    report = []
    total_sales = 0
    total_returns = 0

    for pid in all_products:
        s = sales_dict.get(pid)
        r = returns_dict.get(pid)

        sold_qty = s.total_qty if s else 0
        sales_amt = s.total_sales if s else 0

        returned_qty = r.total_qty if r else 0
        returns_amt = r.total_returns if r else 0

        profit = sales_amt - returns_amt

        report.append({
            "product_id": pid,
            "sold_qty": sold_qty,
            "returned_qty": returned_qty,
            "sales": sales_amt,
            "returns": returns_amt,
            "profit": profit
        })

        total_sales += sales_amt
        total_returns += returns_amt

    return {
        "summary": {
            "total_sales": total_sales,
            "total_returns": total_returns,
            "total_profit": total_sales - total_returns
        },
        "products": report
    }