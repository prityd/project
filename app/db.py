from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:123@cluster0.yi9f0sk.mongodb.net/")

# Check and create database and collection if not exist
db_name = "ecommerce"
product_collection_name = "products"
order_collection_name = "orders"

db = client[db_name]

if product_collection_name not in db.list_collection_names():
    db.create_collection(product_collection_name)
if order_collection_name not in db.list_collection_names():
    db.create_collection(order_collection_name)

products_collection = db[product_collection_name]
orders_collection = db[order_collection_name]
