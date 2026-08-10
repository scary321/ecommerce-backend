from app.database import get_db
from app.config import settings
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.schemas.product import ProductCreate,ProductResponse,ProductUpdate
from app.auth import require_admin, get_current_user
from app.models.products import ProductTable


product_router = APIRouter()

@product_router.post("/products",status_code=status.HTTP_201_CREATED,response_model=ProductResponse)
def create_product(product: ProductCreate,current_user=Depends(require_admin),db: Session = Depends(get_db)):

    new_product= ProductTable(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock,
         category = product.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@product_router.get("/products",response_model=list[ProductResponse])
def get_all_products(current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    
    products = db.query(ProductTable).all()
        
    return products

@product_router.get("/products/{id}",response_model=ProductResponse)
def get_product(id:int, current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    product = db.query(ProductTable).filter(ProductTable.id == id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )
 
    return product 

@product_router.patch("/products/{id}",response_model=ProductResponse)
def update_product(id:int,product_update: ProductUpdate, current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    product = db.query(ProductTable).filter(ProductTable.id == id).first()
    
    if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
    
    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)
            
    db.commit()
    db.refresh(product)
        
    return product

@product_router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_product(id: int, current_user=Depends(require_admin),db:Session = Depends(get_db)):
    product = db.query(ProductTable).filter(ProductTable.id == id).first()
        
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
       
    db.delete(product)
    db.commit()
    
    return