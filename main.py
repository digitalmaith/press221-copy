from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app.api.v1.router import api_router

# Import models so SQLAlchemy discovers them before create_all
import app.models  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "API de gestion du pressing **PRESS 221**.\n\n"
            "Gérez vos employés, clients, types de service et dépôts de vêtements."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["Health"], summary="Vérification de l'état de l'API")
    def health_check():
        return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}

    return app


app = create_app()
