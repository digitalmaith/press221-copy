from fastapi import APIRouter

from app.api.v1.endpoints import employes, clients, services, depots

api_router = APIRouter()

api_router.include_router(employes.router)
api_router.include_router(clients.router)
api_router.include_router(services.router)
api_router.include_router(depots.router)
