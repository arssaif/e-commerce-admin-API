# e-commerce-admin-API

A FastAPI back-end to power an admin dashboard for sales, revenue, and inventory insights.

## Setup

1. Clone repo  
2. Create and edit `.env` with your `DATABASE_URL`  
3. `pip install -r requirements.txt`  
4. Ensure MySQL server is running and the target database (`ecomdb`) exists  
5. Run demo data loader:  
   ```bash
   cd e-commerce-admin-API
   python app/scriptsdemo_data.py
6. Start Server
   ```bash
   cd e-commerce-admin-API
   uvicorn app.main:app --reload
