from app.database import get_db
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.auth import get_current_user
from app.models.cart import CartTable ,CartItemTable
from app.models.products import ProductTable 
from app.schemas.cart import CartItemCreate,CartItemResponse,CartItemUpdate,CartResponse
from app.schemas.orders import OrderItemResponse,OrderResponse
from app.models.orders import OrderTable,OrderItemTable

orders_router=APIRouter()

@orders_router.post("/orders",response_model=OrderResponse)
def add_cart(current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    
    cart = db.query(CartTable).filter(CartTable.user_id == current_user.id).first()
    
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no cart exist")
    
    cart_item = db.query(CartItemTable).filter(CartItemTable.cart_id == cart.id).all()
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="item not exist")
    
    total = 0
    
    for item in cart_item:
        product = db.query(ProductTable).filter(ProductTable.id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not exist")
        
        if item.quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not enough stock")
        
        item_total = product.price * item.quantity
        total += item_total
        
    order = OrderTable(
            user_id = current_user.id,
            total = total
            )
    
    db.add(order)
    db.flush()
    db.refresh(order)
    
    for item in cart_item:
        product = db.query(ProductTable).filter(ProductTable.id == item.product_id).first()
        
        order_item = OrderItemTable(
            product_id = item.product_id,
            quantity = item.quantity,
            price = product.price,
            order_id = order.id
        )
        db.add(order_item)
        
    for item in cart_item:
        product = db.query(ProductTable).filter(ProductTable.id == item.product_id).first()
        
        new_quantity = product.stock - item.quantity
        product.stock=new_quantity   
        
    for item in cart_item:
        db.delete(item)
        
    db.commit()

    return order

@orders_router.get("/orders",response_model=list[OrderResponse])
def get_all_orders(current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    
    get_order=db.query(OrderTable).filter(OrderTable.user_id==current_user.id).all()
    
    if not get_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="orders not found")
    
    return get_order

@orders_router.get("/orders/{id}",response_model=OrderResponse)
def get_order(id:int,current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    
    order=db.query(OrderTable).filter(OrderTable.user_id==current_user.id,OrderTable.id == id).first()
    
    if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
            
    return order