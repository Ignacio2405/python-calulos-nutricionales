"""Registro de rutas HTTP del módulo."""

from fastapi import APIRouter

from core.views import router as views_router

router = APIRouter()
router.include_router(views_router)
