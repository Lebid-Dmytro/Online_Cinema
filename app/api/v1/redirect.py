from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/redirect", tags=["redirect"])


@router.get("/")
async def redirect_root():
    """Base redirect endpoint"""
    return RedirectResponse(url="/docs")

