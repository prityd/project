from fastapi import FastAPI, status, Query
from fastapi.responses import JSONResponse
from app.models import Product, Order
from app.db import products_collection, orders_collection
from bson import ObjectId
from typing import Optional

app = FastAPI()

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    product_dict = product.dict()
    result = products_collection.insert_one(product_dict)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(result.inserted_id)})

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    order_dict = order.dict()
    result = orders_collection.insert_one(order_dict)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(result.inserted_id)})

@app.get("/products")
def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # case-insensitive search

    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    cursor = products_collection.find(query).skip(offset).limit(limit).sort("_id")
    results = []
    for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })

    response = {
        "data": results,
        "page": {
            "next": offset + limit,
            "limit": len(results),
            "previous": max(0, offset - limit)
        }
    }
    return JSONResponse(content=response)

@app.get("/orders/{user_id}")
def get_orders(user_id: str, limit: int = Query(10), offset: int = Query(0)):
    cursor = orders_collection.find({"userId": user_id}).skip(offset).limit(limit)
    data = []

    for order in cursor:
        items = []
        total = 0.0
        for item in order.get("items", []):
            product = products_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                product_details = {
                    "name": product["name"],
                    "id": str(product["_id"])
                }
                items.append({
                    "productDetails": product_details,
                    "qty": item["qty"]
                })
                total += product["price"] * item["qty"]
        data.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total
        })

    return {
        "data": data,
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": str(max(offset - limit, 0))
        }
    }