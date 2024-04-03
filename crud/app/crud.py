from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    db_book =  db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        return db_book
    raise HTTPException(status_code=404, detail="Book not found")


def create_book(db: Session, book: schemas.BookIn) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def remove_book(db: Session, book_id: int) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    raise HTTPException(status_code=404, detail="Book not found")


def update_book(db: Session, book_id: int, title: Optional[str] = None, description: Optional[str] = None) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        if title:
            db_book.title = title
        if description:
            db_book.description = description
        db.commit()
        db.refresh(db_book)
        return db_book
    raise HTTPException(status_code=404, detail="Book not found")
