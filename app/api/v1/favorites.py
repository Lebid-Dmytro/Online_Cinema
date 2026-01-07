from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.movie import Movie, Genre
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteListResponse, FavoriteMovieItem

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/{movie_id}", status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    existing_favorite = db.query(Favorite).filter(
        and_(Favorite.user_id == current_user.id, Favorite.movie_id == movie_id)
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already in favorites"
        )
    
    favorite = Favorite(user_id=current_user.id, movie_id=movie_id)
    db.add(favorite)
    
    try:
        db.commit()
        db.refresh(favorite)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add to favorites"
        )
    
    return {"message": "Movie added to favorites", "favorite_id": favorite.id}


@router.delete("/{movie_id}", status_code=status.HTTP_200_OK)
async def remove_from_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    favorite = db.query(Favorite).filter(
        and_(Favorite.user_id == current_user.id, Favorite.movie_id == movie_id)
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found in favorites"
        )
    
    try:
        db.delete(favorite)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove from favorites"
        )
    
    return {"message": "Movie removed from favorites"}


@router.get("/", response_model=FavoriteListResponse)
async def get_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    year: Optional[int] = Query(None),
    genre_id: Optional[int] = Query(None),
    imdb_min: Optional[float] = Query(None, ge=0, le=10),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None, regex="^(year|imdb|price|added_at)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Movie).join(Favorite).filter(Favorite.user_id == current_user.id)
    
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
        elif sort_by == "added_at":
            order_column = Favorite.added_at
        else:
            order_column = Favorite.added_at
        
        if sort_order == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
    else:
        query = query.order_by(Favorite.added_at.desc())
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    favorites = query.offset((page - 1) * page_size).limit(page_size).all()
    
    favorite_items = []
    for movie in favorites:
        favorite_rel = db.query(Favorite).filter(
            and_(Favorite.user_id == current_user.id, Favorite.movie_id == movie.id)
        ).first()
        
        movie_data = FavoriteMovieItem.model_validate(movie)
        movie_data.added_at = favorite_rel.added_at
        favorite_items.append(movie_data)
    
    return FavoriteListResponse(
        items=favorite_items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
    