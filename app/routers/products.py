from app.database import get_db
from app.config import settings
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.schemas.product import ProductCreate,ProductResponse,ProductUpdate
from app.auth import require_admin
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