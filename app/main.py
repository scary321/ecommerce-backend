from app.routers.users import user_router
from app.routers.products import product_router
from app.routers.cart import cart_router
from fastapi import FastAPI
from app.routers.orders import orders_router
from app.routers.admin import admin_router
from app.routers.payment import payment_router

app = FastAPI()

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(payment_router)