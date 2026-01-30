from fastapi import Depends,FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
import database_models # <--- This imports the WHOLE file as 'database_models'
from models import Product
from sqlalchemy.orm import Session
app = FastAPI()

app.add_middleware(
CORSMiddleware,
origins = [
    "http://localhost:3000",
    "https://intelliims.vercel.app/", # Add your actual Vercel link here
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to fast api project"

products=[
    Product(id=1,name="Phone",description="Budget Phone",price=99,quantity=10),
    Product(id=2,name="Laptop",description="Gaming Laptop",price=999,quantity=5),
    Product(id=3,name="Laptop table",description="Wooden Laptop Table",price=299,quantity=5),
]

def get_db():
    db=session()
    try:    
        yield db
    finally:
        db.close()

def init_db():
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        
        db.commit()



# fetching all records

@app.get("/products")
def get_all_prodcuts(db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products

# fetching one record 
@app.get("/products/{id}")
def get_product_by_id(id: int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    
    return "product not found"


# add products
@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int,product: Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first() #checks for product existence & gives you the product
    if db_product:
        #if element exists, then update all the fields of the element based on user input stored in 'product'
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity 
        db.commit()
        return "product updated"
    else:
        return "no product found"


@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
        db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first() #checks for product existence & gives you the product
        if db_product:
            #if product exists then delete the product
            db.delete(db_product)
            db.commit()
            return "product deleted"
        else:    
            return "product not found"




