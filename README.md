# e-commerce-admin-API

A FastAPI back-end to power an admin dashboard for sales, revenue, and inventory insights.

# Setup

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

# Endpoints

## 1. Products
•	POST /products/

Register new product

•	GET /products/?skip=0&limit=100

List products

## 2. Sales
•	POST /sales/

Record a sale

•	GET /sales/?start=<ISO>&end=<ISO>

Retrieve sales between two datetimes

## 3. Inventory
•	GET /inventory/

View current inventory

•	PUT /inventory/{product_id}?qty=<int>

Set inventory level

# Sample Usage

## 📦 1. Products
### a. Create a product

•	Method: POST

•	Path: /products/

•	Body (JSON):

```bash
{
  "name": "Bluetooth Speaker",
  "category_id": 1,
  "price": 49.99
}
```
•	cURL Example:
```bash
curl -X POST "http://127.0.0.1:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Bluetooth Speaker",
        "category_id": 1,
        "price": 49.99
      }'
```
•	Response (201 Created):
```bash
{
  "id": 12,
  "name": "Bluetooth Speaker",
  "category_id": 1,
  "price": 49.99,
  "category": {
    "id": 1,
    "name": "Electronics"
  }
}
```

### b. List products
•	Method: GET

•	Path: /products/

•	Query params:

   o	skip (int, default 0)

   o	limit (int, default 100)

•	cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/products?skip=0&limit=10" \
  -H "Accept: application/json"
```
•	Response (200 OK):
```bash
[
  {
    "id": 1,
    "name": "Electronics Item 1",
    "category_id": 1,
    "price": 129.99,
    "category": {
      "id": 1,
      "name": "Electronics"
    }
  },
  {
    "id": 2,
    "name": "Clothing Item 1",
    "category_id": 2,
    "price": 29.99,
    "category": {
      "id": 2,
      "name": "Clothing"
    }
  }
  // …
]
```

## 2. 💰 Sales
### a. Record a sale

•	Method: POST

•	Path: /sales/

•	Body (JSON):
```bash
{
  "product_id": 1,
  "quantity": 2,
  "total_price": 259.98,
  "sold_at": "2025-05-17T14:30:00Z"
}
```
•	cURL Example:
```bash
curl -X POST "http://127.0.0.1:8000/sales/" \
  -H "Content-Type: application/json" \
  -d '{
        "product_id": 1,
        "quantity": 2,
        "total_price": 259.98,
        "sold_at": "2025-05-17T14:30:00Z"
      }'
```
•	Response (201 Created):
```bash
{
  "id": 45,
  "product_id": 1,
  "quantity": 2,
  "total_price": 259.98,
  "sold_at": "2025-05-17T14:30:00Z",
  "product": {
    "id": 1,
    "name": "Electronics Item 1",
    "category_id": 1,
    "price": 129.99,
    "category": {
      "id": 1,
      "name": "Electronics"
    }
  }
}
```
### b. Query sales by date range
•	Method: GET

•	Path: /sales/

•	Query params (ISO datetime):

   o	start (e.g. 2025-05-01T00:00:00)

   o	end (e.g. 2025-05-17T23:59:59)

•	cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/sales?start=2025-05-01T00:00:00&end=2025-05-17T23:59:59" \
  -H "Accept: application/json"
```
•	Response (200 OK):
```bash
[
  {
    "id": 42,
    "product_id": 3,
    "quantity": 1,
    "total_price": 19.99,
    "sold_at": "2025-05-05T10:15:00Z",
    "product": { /* product details */ }
  },
  {
    "id": 44,
    "product_id": 1,
    "quantity": 2,
    "total_price": 259.98,
    "sold_at": "2025-05-12T14:00:00Z",
    "product": { /* product details */ }
  }
  // …
]
```

## 3. 📦 Inventory
### a. View inventory status

•	Method: GET

•	Path: /inventory/

•	cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/inventory/" \
  -H "Accept: application/json"
```
•	Response (200 OK):
```bash
[
  {
    "id": 1,
    "product_id": 1,
    "quantity": 18,
    "last_updated": "2025-05-17T14:31:00Z",
    "product": { /* product details */ }
  },
  {
    "id": 2,
    "product_id": 2,
    "quantity": 50,
    "last_updated": "2025-05-17T14:00:00Z",
    "product": { /* product details */ }
  }
  // …
]
```

### b. Update inventory level
•	Method: PUT

•	Path: /inventory/{product_id}

•	Query param:

   o	qty (int, new stock level)

•	cURL Example:
```bash
curl -X PUT "http://127.0.0.1:8000/inventory/1?qty=75" \
  -H "Accept: application/json"
```
•	Response (200 OK):
```bash
{
  "id": 1,
  "product_id": 1,
  "quantity": 75,
  "last_updated": "2025-05-17T15:00:00Z",
  "product": { /* product details */ }
}
```
