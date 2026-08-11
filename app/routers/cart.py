from app.database import get_db
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.auth import get_current_user
from app.models.cart import CartTable ,CartItemTable
from app.models.products import ProductTable
from app.schemas.cart import CartItemCreate,CartItemResponse,CartItemUpdate,CartResponse



cart_router=APIRouter()

@cart_router.post("/cart/items",status_code=status.HTTP_201_CREATED,response_model=CartItemResponse)
def add_items(cart: CartItemCreate,current_user=Depends(get_current_user),db: Session = Depends(get_db)):

    product = db.query(ProductTable).filter(ProductTable.id == cart.product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    if cart.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Quantity must be greater than 0")

    if cart.quantity > product.stock:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail="Not enough stock")

    current_cart = db.query(CartTable).filter(CartTable.user_id == current_user.id).first()


    if not current_cart:
        current_cart = CartTable(
            user_id=current_user.id
        )

        db.add(current_cart)
        db.commit()
        db.refresh(current_cart)

    cart_item = db.query(CartItemTable).filter(CartItemTable.cart_id == current_cart.id,CartItemTable.product_id == cart.product_id).first()

    if cart_item:
        new_quantity = cart_item.quantity + cart.quantity

        if new_quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not enough stock")

        cart_item.quantity = new_quantity

    else:
        cart_item = CartItemTable(
            cart_id=current_cart.id,
            product_id=cart.product_id,
            quantity=cart.quantity
        )

        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item

@cart_router.get("/cart",response_model=CartResponse)
def get_all_cart_item(current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    
    get_cart =db.query(CartTable).filter(current_user.id==CartTable.user_id).first()
    
    if not get_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart is empty")
    
    get_cartitem =db.query(CartItemTable).filter(CartItemTable.cart_id==get_cart.id).all()
    
    items = []
    total = 0

    for cart_item in get_cartitem:
        product = db.query(ProductTable).filter(ProductTable.id == cart_item.product_id).first()

        if not product:
            continue

        subtotal = product.price * cart_item.quantity
        total += subtotal

        items.append(
            CartItemResponse(id=cart_item.id,product_id=cart_item.product_id,quantity=cart_item.quantity)
        )

    return CartResponse(id=get_cart.id,items=items,total=total)