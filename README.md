# Canteen API - LAB 5

## 1. Giới thiệu
REST API quản lý món ăn căng tin bằng FastAPI.
Hỗ trợ CRUD và kiểm thử bằng Postman, Newman.

## 2. Công nghệ sử dụng
- Python
- FastAPI
- Pydantic
- Uvicorn
- Postman
- Newman

## 3. Cài đặt
Tạo môi trường ảo và cài thư viện:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## 4. Chạy API

    python -m uvicorn app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

## 5. Kiểm thử Newman

    newman run "postman/LAB5 - Canteen CRUD API.postman_collection.json" -e "postman/LAB5 - Local.postman_environment.json" --folder "CSV Tests" -d "postman/negative.csv" --reporters cli

Kết quả kiểm thử: 6/6 test PASS.

## 6. Cấu trúc dự án
- app/: Mã nguồn FastAPI
- docs/: Ảnh minh chứng
- postman/: Collection, Environment và dữ liệu CSV
- requirements.txt: Danh sách thư viện Python
- .gitignore: Các file không đưa lên Git
