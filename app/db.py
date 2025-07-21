from pymongo import MongoClient
import certifi

#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb+srv://admin:123@cluster0.yi9f0sk.mongodb.net/", tls=True,
    tlsCAFile=certifi.where())

# Check and create database and collection if not exist
db_name = "ecommerce"

#collections
product_collection_name = "products"
order_collection_name = "orders"


db = client[db_name]

if product_collection_name not in db.list_collection_names():
    db.create_collection(product_collection_name)

if order_collection_name not in db.list_collection_names():
    db.create_collection(order_collection_name)

products_collection = db[product_collection_name]
orders_collection = db[order_collection_name]
