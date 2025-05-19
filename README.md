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
   python app/scripts/load_demo_data.py
6. Start Server
   ```bash
   cd e-commerce-admin-API
   uvicorn app.main:app --reload

# Endpoints

## 1. Products
a.	POST /products/
   - Register new product

b.	GET /products/?skip=0&limit=100
   - List products

## 2. Sales
a.	POST /sales/
   - Record a sale

b.	GET /sales/?start=<ISO>&end=<ISO>[&product_id=<int>][&category_id=<int>] 
   - Retrieve sales between two datetimes

c.	GET /sale/revenue/?start=<ISO>&end=<ISO>[&period=<daily|weekly|monthly|yearly>][&category_id=<int>]
   - Retries revenue grouped by period (daily/weekly/monthly)
     
d. GET /sales/revenue/compare/?p1_start=<ISO>&p1_end=<ISO>&p2_start=<ISO>&p2_end=<ISO>[&period=<daily|weekly|monthly|yearly>][&category_id=<int>]
   - Compare revenue for two date ranges, grouped by the given interval
     
## 3. Inventory
a.	GET /inventory/
   - View current inventory

b.	PUT /inventory/{product_id}?qty=<int>
   - Set inventory level

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
   - `skip` (int, default 0)
   - `limit` (int, default 100)

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
   - `start` (e.g. 2025-05-01T00:00:00)
   - `end`   (e.g. 2025-05-17T23:59:59)
   - `product_id` (int, optional)  
   - `category_id` (int, optional) 

•	cURL Example:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/sales/?start=2025-04-19T09%3A51%3A54.333Z&end=2025-05-20T09%3A51%3A54.333Z&product_id=41&category_id=2' \
  -H 'accept: application/json'
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
### c. Revenue report

• Method: GET  
• Path: `/sales/revenue/`  
• Query params:  
  - `start` (ISO datetime, required)  
  - `end` (ISO datetime, required)  
  - `period` (daily / weekly / monthly / yearly, default “daily”)  
  - `category_id` (int, optional)  

• cURL Example:  
```bash
curl -X GET "http://127.0.0.1:8000/sales/revenue/?\
start=2025-04-01T00:00:00&\
end=2025-05-31T23:59:59&\
period=monthly&\
category_id=2" \
  -H "Accept: application/json"
```
•	Response (200 OK):
```bash
[
  { "period": 4, "revenue": 19170.24 },
  { "period": 5, "revenue": 69605.02 }
]
```

### d. Compare revenue between two date ranges
• Method: GET
• Path: /sales/revenue/compare/
• Query params:
   - `p1_start` (ISO datetime, required)
   - `p1_end` (ISO datetime, required)
   - `p2_start` (ISO datetime, required)
   - `p2_end` (ISO datetime, required)
   - `period` (daily / weekly / monthly / yearly, default “monthly”)

category_id (int, optional)

• cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/sales/revenue/compare/?\
p1_start=2025-04-01T00:00:00&\
p1_end=2025-04-30T23:59:59&\
p2_start=2025-05-01T00:00:00&\
p2_end=2025-05-31T23:59:59&\
period=monthly&\
category_id=2" \
  -H "Accept: application/json"
```
• Response (200 OK):
```bash
{
  "period1": [
    { "period": 4, "revenue": 19170.24 }
  ],
  "period2": [
    { "period": 5, "revenue": 69605.02 }
  ]
}
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
   - `qty` (int, new stock level)

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
