from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.database import get_db
from app.schemas.user import UserResponse ,AdminRoleUpdate
from app.auth import require_admin
from app.models.user import UsersTable
from app.schemas.orders import OrderResponse
from app.models.orders import OrderTable
from app.schemas.orders import StatusUpdate
from app.models.orders import OrderTable,OrderItemTable
from app.models.products import ProductTable
from app.schemas.dashboard import DashboardResponse
from sqlalchemy import func



admin_router=APIRouter()



@admin_router.get("/users",response_model=list[UserResponse])
def admin_user(current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    users = db.query(UsersTable).all()
    
    return users

@admin_router.put("/users/{id}",response_model=UserResponse)
def admin_update_user(id:int,role_update:AdminRoleUpdate,current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    user = db.query(UsersTable).filter(UsersTable.id == id).first()

    if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
    
    user.role = role_update.role
    
    db.commit()
    db.refresh(user)
        
    return user

@admin_router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(id: int, current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    user = db.query(UsersTable).filter(UsersTable.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if current_user.id == id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin cannot delete themselves")

    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Cannot delete another admin")

    db.delete(user)
    db.commit()

    return

@admin_router.get("/admin/orders",response_model=list[OrderResponse])
def get_all_orders(status: str | None = None,current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    orders = db.query(OrderTable)
    
    status_order = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    if status:
        if status not in status_order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )

        orders = orders.filter(OrderTable.status == status)

    return orders.all()

@admin_router.patch("/orders/{id}/status",response_model=OrderResponse)
def admin_update_status(id:int,status_update: StatusUpdate,current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    order=db.query(OrderTable).filter(OrderTable.id == id).first()
        
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
        
    status_order=["pending","processing","shipped","delivered","cancelled"]
    
    if status_update.status not in status_order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid status")
                
    order.status = status_update.status    
        
    db.commit()
    db.refresh(order)
    return order

@admin_router.patch("/orders/{id}/cancel",response_model=OrderResponse)
def update_status(id:int,current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    order=db.query(OrderTable).filter(OrderTable.id == id).first()
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    
    if order.status in ["cancelled"] :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail ="reject cancellation")
    
    if order.status in ["delivered"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail ="reject cancellation beacause order already deliverd")
     
    order_item = db.query(OrderItemTable).filter(OrderItemTable.order_id==order.id).all()

    for item in order_item:
        product =db.query(ProductTable).filter(ProductTable.id == item.product_id).first()
        product.stock += item.quantity
    order.status = "cancelled"
        
    db.commit()
    db.refresh(order)
    return order

@admin_router.get("/admin/dashboard",response_model=DashboardResponse)
def admin_dashboard(current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    total_user=db.query(UsersTable).count()
    total_product=db.query(ProductTable).count()
    total_orders=db.query(OrderTable).count()
    total_pending_orders=db.query(OrderTable).filter(OrderTable.status=="pending").count()
    total_processing_orders=db.query(OrderTable).filter(OrderTable.status=="processing").count()
    total_shipped_orders=db.query(OrderTable).filter(OrderTable.status=="shipped").count()
    total_delivered_orders=db.query(OrderTable).filter(OrderTable.status=="delivered").count()
    total_cancelled_orders= db.query(OrderTable).filter(OrderTable.status=="cancelled").count()
    total_sales = db.query(func.sum(OrderTable.total)).filter(OrderTable.status != "cancelled").scalar() or 0
    
    return DashboardResponse(
    users=total_user,
    products=total_product,
    orders=total_orders,
    pending_orders=total_pending_orders,
    processing_orders=total_processing_orders,
    shipped_orders=total_shipped_orders,
    delivered_orders=total_delivered_orders,
    cancelled_orders=total_cancelled_orders,
    sales=total_sales
)