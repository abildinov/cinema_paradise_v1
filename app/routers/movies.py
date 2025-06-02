from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models import Movie as MovieModel
from ..schemas import Movie, MovieCreate, MovieUpdate, MovieList

router = APIRouter()

@router.post("/", response_model=Movie, summary="Создать фильм")
async def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового фильма в базе данных.
    
    - **title**: Название фильма (обязательно)
    - **description**: Описание фильма
    - **duration_minutes**: Продолжительность в минутах
    - **genre**: Жанр фильма
    - **director**: Режиссер
    - **release_year**: Год выпуска
    - **rating**: Рейтинг (0-10)
    - **poster_url**: URL постера
    """
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=MovieList, summary="Получить список фильмов")
async def get_movies(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей на странице"),
    search: Optional[str] = Query(None, description="Поиск по названию или режиссеру"),
    genre: Optional[str] = Query(None, description="Фильтр по жанру"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    db: Session = Depends(get_db)
):
    """
    Получение списка фильмов с возможностью фильтрации и поиска.
    """
    query = db.query(MovieModel)
    
    if search:
        query = query.filter(
            (MovieModel.title.ilike(f"%{search}%")) |
            (MovieModel.director.ilike(f"%{search}%"))
        )
    
    if genre:
        query = query.filter(MovieModel.genre.ilike(f"%{genre}%"))
    
    if is_active is not None:
        query = query.filter(MovieModel.is_active == is_active)
    
    total = query.count()
    movies = query.offset(skip).limit(limit).all()
    
    return MovieList(
        movies=movies,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )

@router.get("/{movie_id}", response_model=Movie, summary="Получить фильм по ID")
async def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного фильма по его ID.
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@router.put("/{movie_id}", response_model=Movie, summary="Обновить фильм")
async def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновление данных фильма.
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    update_data = movie_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        for field, value in update_data.items():
            setattr(movie, field, value)
        
        db.commit()
        db.refresh(movie)
    
    return movie

@router.delete("/{movie_id}", summary="Удалить фильм")
async def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаление фильма из базы данных.
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    db.delete(movie)
    db.commit()
    return {"message": "Фильм успешно удален"}

@router.get("/{movie_id}/sessions", summary="Получить сеансы фильма")
async def get_movie_sessions(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение всех сеансов конкретного фильма.
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    return movie.sessions 