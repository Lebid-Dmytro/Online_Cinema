from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from app.schemas.movie import GenreResponse, CertificationResponse


class FavoriteMovieItem(BaseModel):
    id: int
    uuid: UUID
    name: str
    year: int
    time: int
    imdb: float
    price: Decimal
    certification: CertificationResponse
    genres: List[GenreResponse]
    added_at: datetime

    class Config:
        from_attributes = True


class FavoriteListResponse(BaseModel):
    items: List[FavoriteMovieItem]
    total: int
    page: int
    page_size: int
    total_pages: int

