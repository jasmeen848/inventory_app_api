from fastapi import FastAPI, APIRouter
from app.api import customer_details, inventory_details, booking_details, admin_details, login

app = FastAPI()

api_router = APIRouter()

api_router.include_router(customer_details.router, prefix='', tags=["customer"])
api_router.include_router(inventory_details.router, prefix='', tags=["inventory"])
api_router.include_router(booking_details.router, prefix='', tags=["booking"])
api_router.include_router(admin_details.router, prefix='', tags=["admin"])
api_router.include_router(login.router, prefix='', tags=["login"])

app.include_router(api_router, prefix='')

