from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from uuid import UUID


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StarResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DirectorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CertificationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieBase(BaseModel):
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: Decimal
    certification_id: int


class MovieCreate(MovieBase):
    genre_ids: List[int] = []
    director_ids: List[int] = []
    star_ids: List[int] = []


class MovieUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    time: Optional[int] = None
    imdb: Optional[float] = None
    votes: Optional[int] = None
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    certification_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None
    director_ids: Optional[List[int]] = None
    star_ids: Optional[List[int]] = None


class MovieResponse(BaseModel):
    id: int
    uuid: UUID
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    description: str
    price: Decimal
    certification: CertificationResponse
    genres: List[GenreResponse]
    directors: List[DirectorResponse]
    stars: List[StarResponse]

    class Config:
        from_attributes = True


class MovieListItem(BaseModel):
    id: int
    uuid: UUID
    name: str
    year: int
    time: int
    imdb: float
    price: Decimal
    certification: CertificationResponse
    genres: List[GenreResponse]

    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    items: List[MovieListItem]
    total: int
    page: int
    page_size: int
    total_pages: int

