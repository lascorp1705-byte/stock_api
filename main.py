from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Product
from schemas import ProductCreate, ShipmentCreate

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Management API",
    description="API for managing warehouse shipments",
    version="1.0.0"
)


# 1. Add a product
@app.post("/products")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        qty_sent=product.qty_sent,
        qty_received=product.qty_received
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product created successfully",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "qty_sent": new_product.qty_sent,
            "qty_received": new_product.qty_received
        }
    }


# 2. Add a shipment movement
@app.post("/products/{product_id}/shipment")
def register_shipment(
    product_id: int,
    shipment: ShipmentCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.qty_sent += shipment.qty_sent
    product.qty_received += shipment.qty_received

    db.commit()
    db.refresh(product)

    return {
        "message": "Shipment movement added successfully",
        "product_id": product.id,
        "qty_sent": product.qty_sent,
        "qty_received": product.qty_received
    }


# 3. Calculate shipment difference
@app.get("/products/{product_id}/difference")
def calculate_difference(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    difference = product.qty_sent - product.qty_received

    if difference == 0:
        status = "مطابقة"
    elif difference > 0:
        status = "عجز"
    else:
        status = "فائض"

    return {
        "product_id": product.id,
        "product_name": product.name,
        "qty_sent": product.qty_sent,
        "qty_received": product.qty_received,
        "difference": difference,
        "status": status
    }


# 4. Get all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):

    return db.query(Product).all()