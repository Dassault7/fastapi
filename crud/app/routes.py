from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status

from app import crud, schemas
from app.db import get_db


router = APIRouter()


@router.get("/books", responses={
    200: {"model": list[schemas.BookInDBBase], "description": "Get all books"}
})
async def get_books(db: Session = Depends(get_db)):
    """
    Get all books
    """
    
    return crud.get_books(db)


@router.get("/books/{book_id}", responses={
    200: {"model": schemas.BookInDBBase, "description": "Get book by id"},
    404: {"description": "Book not found"}
})
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Get book by id
    """
    
    return crud.get_book_by_id(db, book_id)


@router.post("/books", status_code=201, responses={
    201: {"model": schemas.BookInDBBase, "description": "Create a new book"}
})
async def create_book(book: schemas.BookIn, db: Session = Depends(get_db)):
    """
    Create a new book
    """
    
    return crud.create_book(db, book)


@router.delete("/{book_id}", responses={
    200: {"model": schemas.BookInDBBase, "description": "Delete book by id"},
    404: {"description": "Book not found"}
})
async def remove_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete book by id
    """
    
    return crud.remove_book(db, book_id)


@router.patch("/books/{book_id}", responses={
    200: {"model": schemas.BookInDBBase, "description": "Update book by id"},
    404: {"description": "Book not found"}
})
async def update_book(book_id: int, title: str = None, description: str = None, db: Session = Depends(get_db)):
    """
    Update book by id
    """
    
    return crud.update_book(db, book_id, title, description)

