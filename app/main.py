from app.routers.users import user_router
from app.routers.products import product_router
from app.routers.cart import cart_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)