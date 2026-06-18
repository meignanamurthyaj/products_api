from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

import database
import models
import schemas
import crud

# Initialize tables automatically on app start
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Product Management API")

# Global Exception Fallback
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred.", "error": str(exc)},
    )

@app.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, product)

@app.get("/products", response_model=List[schemas.ProductResponse])
def read_all_products(db: Session = Depends(database.get_db)):
    return crud.get_products(db)

@app.get("/products/{id}", response_model=schemas.ProductResponse)
def read_product_by_id(id: int, db: Session = Depends(database.get_db)):
    product = crud.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return product

@app.put("/products/{id}", response_model=schemas.ProductResponse)
def modify_product(id: int, product_update: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    product = crud.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return crud.update_product(db, product, product_update)

@app.delete("/products/{id}", status_code=status.HTTP_200_OK)
def remove_product(id: int, db: Session = Depends(database.get_db)):
    product = crud.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    crud.delete_product(db, product)
    return {"detail": f"Product with ID {id} has been successfully deleted."}