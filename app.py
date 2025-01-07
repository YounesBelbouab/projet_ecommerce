from fastapi import  FastAPI
from pymongo import MongoClient
import uvicorn

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['ecomerce']
@app.get("/ecommerce/sales-by-city")
async def get_sales_by_city():
    result = list(db['orders'].aggregate([
        {
            '$lookup': {
                'from': 'location',
                'localField': 'Postal Code',
                'foreignField': 'Postal Code',
                'as': 'locationDetails'
            }
        },
        {'$unwind': '$locationDetails'},
        {
            '$group': {
                '_id': '$locationDetails.City',
                'totalSales': {'$sum': 1}
            }
        },
        {'$sort': {'totalSales': -1}}
    ]))
    return {"sales_by_city": result}

@app.get("/ecommerce/total-orders")
async def get_total_orders():
    result = list(db['orders'].aggregate([
        {
            '$group': {
                '_id': None,
                'totalOrders': {'$sum': 1}
            }
        }
    ]))
    return {"total_orders": result[0]['totalOrders'] if result else 0}

@app.get("/ecommerce/sales-by-ship-mode")
async def get_sales_by_ship_mode():
    result = list(db['orders'].aggregate([
        {
            '$group': {
                '_id': '$Ship Mode',
                'totalSales': {'$sum': '$Sales'}
            }
        },
        {'$sort': {'totalSales': -1}}
    ]))
    return {"sales_by_ship_mode": result}

@app.get("/ecommerce/average-basket")
async def get_average_basket():
    result = list(db['orders'].aggregate([
        {
            '$group': {
                '_id': None,
                'totalSales': {'$sum': '$Sales'},
                'totalOrders': {'$sum': 1}
            }
        },
        {
            '$project': {
                '_id': 0,
                'averageBasket': {
                    '$divide': ['$totalSales', '$totalOrders']
                }
            }
        }
    ]))
    return {"average_basket": result[0]['averageBasket'] if result else 0}

@app.get("/ecommerce/sales-by-product")
async def get_sales_by_product():
    result = list(db['orders'].aggregate([
        {
            '$lookup': {
                'from': 'products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'productDetails'
            }
        },
        {'$unwind': '$productDetails'},
        {
            '$group': {
                '_id': '$productDetails.Product Name',
                'totalQuantity': {'$sum': '$Quantity'},
                'totalSales': {'$sum': '$Sales'}
            }
        }
    ]))
    return {"sales_by_product": result}

@app.get("/ecommerce/sales-by-state")
async def get_sales_by_state():
    result = list(db['orders'].aggregate([
        {
            '$lookup': {
                'from': 'location',
                'localField': 'Postal Code',
                'foreignField': 'Postal Code',
                'as': 'locationDetails'
            }
        },
        {'$unwind': '$locationDetails'},
        {
            '$group': {
                '_id': '$locationDetails.State',
                'totalSales': {'$sum': '$Sales'}
            }
        },
        {'$sort': {'totalSales': -1}}
    ]))
    return {"sales_by_state": result}

@app.get("/ecommerce/sales-by-customer")
async def get_sales_by_customer():
    result = list(db['Orders'].aggregate([
        {
            '$lookup': {
                'from': 'Customers',
                'localField': 'Customer ID',
                'foreignField': 'Customer ID',
                'as': 'customerDetails'
            }
        },
        {'$unwind': '$customerDetails'},
        {
            '$group': {
                '_id': '$Customer ID',
                'customer_name': {'$first': '$customerDetails.Customer Name'},
                'total_sales': {'$sum': '$Sales'}
            }
        },
        {'$sort': {'total_sales': -1}}
    ]))
    return {"sales_by_customer": result}

@app.get("/ecommerce/sales-by-post-code")
async  def get_sales_by_post_code():
    result = list(client['ecomerce']['orders'].aggregate([
        {
            '$group': {
                '_id': '$Postal Code',
                'total_sales': {
                    '$sum': '$Sales'
                }
            }
        }, {
            '$sort': {
                'total_sales': -1
            }
        }
    ]))
    return {"sales_by_code_post": result}

@app.get("/ecommerce/average-cart")
async def average_cart():
    result = list(client['ecomerce']['orders'].aggregate([
        {
            '$group': {
                '_id': None,
                'total_sales': {
                    '$sum': '$Sales'
                },
                'order_count': {
                    '$sum': 1
                }
            }
        }, {
            '$project': {
                'average_basket': {
                    '$divide': [
                        '$total_sales', '$order_count'
                    ]
                }
            }
        }
    ]))
    return {"panier moyen" : result}

@app.get("/ecommerce/total-sales")
async def totale_sales():
    result = list(client['ecomerce']['orders'].aggregate([
        {
            '$group': {
                '_id': '$Product Category',
                'total_sales': {
                    '$sum': '$Sales'
                }
            }
        }, {
            '$sort': {
                'total_sales': -1
            }
        }
    ]))
    return {"total des ventes" : result}

@app.get("/ecommerce/nombre-commande-moyenne-par-client")
async def average_order_by_client():
    result = list(client['ecomerce']['orders'].aggregate([
        {
            '$group': {
                '_id': '$Customer ID',
                'order_count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': None,
                'average_orders_per_customer': {
                    '$avg': '$order_count'
                }
            }
        }
    ]))
    return {"nombre de commande moyenne par client" : result}

@app.get("/ecommerce/average-product-by-sales")
async def average_product_by_sales():
    result = list(client['ecomerce']['orders'].aggregate([
        {
            '$group': {
                '_id': None,
                'totalQuantity': {
                    '$sum': '$Quantity'
                },
                'totalOrders': {
                    '$sum': 1
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'averageProductsPerOrder': {
                    '$divide': [
                        '$totalQuantity', '$totalOrders'
                    ]
                }
            }
        }
    ]))
    return {"nombre de produit moyen par vente" : result}

@app.get("/ecommerce/sales-by-category")
async def get_sales_by_category():
    pipeline = [
        # Jointure entre orders et products sur le Product ID
        {
            "$lookup": {
                "from": "products",
                "localField": "Product ID",  # Champ dans 'orders'
                "foreignField": "Product ID",  # Champ dans 'products'
                "as": "productDetails"
            }
        },
        {"$unwind": "$productDetails"},  # Décomparer le tableau résultant de la jointure
        {
            "$group": {
                "_id": "$productDetails.Category",  # Grouper par catégorie de produit
                "totalSales": {"$sum": "$Sales"},  # Somme des ventes par catégorie
                "totalQuantity": {"$sum": "$Quantity"}  # Total des quantités vendues par catégorie
            }
        },
        {"$sort": {"totalSales": -1}}  # Trier les résultats par les ventes totales décroissantes
    ]

    # Exécution de l'agrégation sur la collection orders
    data = db['orders'].aggregate(pipeline)

    # Formatage des résultats
    result = [
        {
            "category": item["_id"],  # Nom de la catégorie
            "total_sales": item["totalSales"],  # Ventes totales pour la catégorie
            "total_quantity": item["totalQuantity"]  # Quantité totale vendue pour la catégorie
        }
        for item in data
    ]

    return {"sales_by_category": result}

@app.get("/ecommerce/sales-by-date")
async def get_sales_by_date():
    # Pipeline d'agrégation simplifié
    pipeline = [
        {
            "$group": {
                "_id": "$Order Date",  # Utilisation de la date brute comme clé
                "total_sales": {"$sum": "$Sales"},  # Somme des ventes
                "total_orders": {"$sum": 1}  # Nombre total de commandes
            }
        },
        {
            "$sort": {"_id": 1}  # Tri par date croissante
        }
    ]

    # Exécution du pipeline d'agrégation
    data = db['orders'].aggregate(pipeline)

    # Conversion des données en une liste formatée
    result = [
        {
            "date": item["_id"],  # La date brute telle qu'elle est dans MongoDB
            "total_sales": item.get("total_sales", 0),
            "total_orders": item.get("total_orders", 0)
        }
        for item in data
    ]

    return {"sales_by_date": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)