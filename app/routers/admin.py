from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.database import get_db
from app.schemas.user import UserResponse ,AdminRoleUpdate
from app.auth import require_admin
from app.models.user import UsersTable





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