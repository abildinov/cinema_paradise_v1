from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..database import get_db
from ..models import Review as ReviewModel, Movie as MovieModel, User
from ..auth import get_current_user

router = APIRouter()

class ReviewBase(BaseModel):
    movie_id: int = Field(..., description="ID фильма")
    rating: int = Field(..., ge=1, le=10, description="Рейтинг (1-10)")
    title: Optional[str] = Field(None, max_length=255, description="Заголовок отзыва")
    content: Optional[str] = Field(None, description="Текст отзыва")
    is_spoiler: bool = Field(False, description="Содержит спойлеры")

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=10)
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    is_spoiler: Optional[bool] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    user_name: str
    is_verified_purchase: bool
    helpful_votes: int
    unhelpful_votes: int
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=ReviewResponse, summary="Создать отзыв")
async def create_review(
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создание отзыва о фильме авторизованным пользователем.
    
    - **movie_id**: ID фильма
    - **rating**: Рейтинг от 1 до 10
    - **title**: Заголовок отзыва (опционально)
    - **content**: Текст отзыва (опционально)
    - **is_spoiler**: Отметка о спойлерах
    """
    # Проверяем существование фильма
    movie = db.query(MovieModel).filter(MovieModel.id == review.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    # Проверяем, есть ли уже отзыв от этого пользователя на этот фильм
    existing_review = db.query(ReviewModel).filter(
        ReviewModel.movie_id == review.movie_id,
        ReviewModel.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=400, 
            detail="Вы уже оставили отзыв на этот фильм"
        )
    
    # Проверяем, покупал ли пользователь билет на этот фильм
    from ..models import Ticket, Session
    user_ticket = db.query(Ticket).join(Session).filter(
        Session.movie_id == review.movie_id,
        Ticket.user_id == current_user.id,
        Ticket.status == "used"
    ).first()
    
    is_verified_purchase = user_ticket is not None
    
    # Создаем отзыв
    db_review = ReviewModel(
        **review.dict(),
        user_id=current_user.id,
        is_verified_purchase=is_verified_purchase
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Добавляем имя пользователя для ответа
    response_data = db_review.__dict__.copy()
    response_data["user_name"] = f"{current_user.first_name} {current_user.last_name}"
    
    return ReviewResponse(**response_data)

@router.get("/movie/{movie_id}", response_model=List[ReviewResponse], summary="Получить отзывы о фильме")
async def get_movie_reviews(
    movie_id: int,
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(50, ge=1, le=100, description="Количество записей на странице"),
    sort_by: str = Query("created_at", description="Сортировка: created_at, rating, helpful_votes"),
    order: str = Query("desc", description="Порядок: asc, desc"),
    verified_only: bool = Query(False, description="Только подтвержденные покупки"),
    db: Session = Depends(get_db)
):
    """
    Получение отзывов о конкретном фильме с возможностью сортировки и фильтрации.
    """
    # Проверяем существование фильма
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    query = db.query(ReviewModel).filter(
        ReviewModel.movie_id == movie_id,
        ReviewModel.is_approved == True
    )
    
    if verified_only:
        query = query.filter(ReviewModel.is_verified_purchase == True)
    
    # Сортировка
    if sort_by == "rating":
        sort_field = ReviewModel.rating
    elif sort_by == "helpful_votes":
        sort_field = ReviewModel.helpful_votes
    else:
        sort_field = ReviewModel.created_at
    
    if order == "asc":
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())
    
    reviews = query.offset(skip).limit(limit).all()
    
    # Добавляем информацию о пользователях
    result = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        review_data = review.__dict__.copy()
        review_data["user_name"] = f"{user.first_name} {user.last_name}" if user else "Неизвестный пользователь"
        result.append(ReviewResponse(**review_data))
    
    return result

@router.get("/{review_id}", response_model=ReviewResponse, summary="Получить отзыв по ID")
async def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного отзыва по его ID.
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    user = db.query(User).filter(User.id == review.user_id).first()
    review_data = review.__dict__.copy()
    review_data["user_name"] = f"{user.first_name} {user.last_name}" if user else "Неизвестный пользователь"
    
    return ReviewResponse(**review_data)

@router.put("/{review_id}", response_model=ReviewResponse, summary="Обновить отзыв")
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновление отзыва (только автором отзыва).
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    # Проверяем, что пользователь - автор отзыва
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Вы можете редактировать только свои отзывы"
        )
    
    update_data = review_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        for field, value in update_data.items():
            setattr(review, field, value)
        
        db.commit()
        db.refresh(review)
    
    review_data = review.__dict__.copy()
    review_data["user_name"] = f"{current_user.first_name} {current_user.last_name}"
    
    return ReviewResponse(**review_data)

@router.delete("/{review_id}", summary="Удалить отзыв")
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удаление отзыва (только автором отзыва или администратором).
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    # Проверяем права доступа
    if review.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Недостаточно прав для удаления отзыва"
        )
    
    db.delete(review)
    db.commit()
    return {"message": "Отзыв успешно удален"}

@router.post("/{review_id}/vote", summary="Проголосовать за полезность отзыва")
async def vote_review(
    review_id: int,
    helpful: bool = Query(..., description="True - полезный, False - бесполезный"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Голосование за полезность отзыва.
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    # Проверяем, что пользователь не голосует за свой отзыв
    if review.user_id == current_user.id:
        raise HTTPException(
            status_code=400, 
            detail="Вы не можете голосовать за свой отзыв"
        )
    
    # В реальном приложении здесь была бы отдельная таблица для голосов
    # Для демонстрации просто увеличиваем счетчики
    if helpful:
        review.helpful_votes += 1
    else:
        review.unhelpful_votes += 1
    
    db.commit()
    
    return {
        "message": "Голос учтен",
        "helpful_votes": review.helpful_votes,
        "unhelpful_votes": review.unhelpful_votes
    }

@router.get("/user/my-reviews", response_model=List[ReviewResponse], summary="Мои отзывы")
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение всех отзывов текущего пользователя.
    """
    reviews = db.query(ReviewModel).filter(
        ReviewModel.user_id == current_user.id
    ).order_by(ReviewModel.created_at.desc()).all()
    
    result = []
    for review in reviews:
        review_data = review.__dict__.copy()
        review_data["user_name"] = f"{current_user.first_name} {current_user.last_name}"
        result.append(ReviewResponse(**review_data))
    
    return result 