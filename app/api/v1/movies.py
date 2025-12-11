from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.core.database import get_db
from app.models.movie import Movie, Genre
from app.schemas.movie import MovieResponse, MovieListResponse, MovieListItem

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponse)
async def get_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    year: Optional[int] = Query(None),
    genre_id: Optional[int] = Query(None),
    imdb_min: Optional[float] = Query(None, ge=0, le=10),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None, regex="^(year|imdb|price)$"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Movie)

    if year:
        query = query.filter(Movie.year == year)

    if genre_id:
        query = query.join(Movie.genres).filter(Genre.id == genre_id)

    if imdb_min:
        query = query.filter(Movie.imdb >= imdb_min)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Movie.name.ilike(search_term))

    if sort_by:
        if sort_by == "year":
            order_column = Movie.year
        elif sort_by == "imdb":
            order_column = Movie.imdb
        elif sort_by == "price":
            order_column = Movie.price
        else:
            order_column = Movie.id

        if sort_order == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
    else:
        query = query.order_by(Movie.year.desc())

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    movies = query.offset((page - 1) * page_size).limit(page_size).all()

    return MovieListResponse(
        items=[MovieListItem.model_validate(movie) for movie in movies],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie

