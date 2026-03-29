from fastapi import FastAPI
import auth, product, billing, return_service, report

app = FastAPI(title="Monolith Store")

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(billing.router)
app.include_router(return_service.router)
app.include_router(report.router)