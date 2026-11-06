
from fastapi import FastAPI

from app.routers.menu import router as menu_router

app = FastAPI(
    title="Canteen API - LAB 5",
    description="API CRUD quản lý món ăn căng tin, kiểm thử bằng Postman",
    version="1.0.0",
)

app.include_router(menu_router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Canteen API LAB 5 is running",
        "docs": "/docs",
    }
