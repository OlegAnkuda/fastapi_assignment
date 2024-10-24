from typing import Optional, Annotated
from fastapi import Query, Path, APIRouter
from pydantic import PositiveInt
from fastapi.exceptions import HTTPException
from fastapi.responses import Response

from src.schemas import Book, BookToPatch
from src.database import books_db


router = APIRouter()


@router.post("/books/")
async def post_book(book: Book):
    for book_db in books_db.values():
         if book_db.isbn == book.isbn:
             raise HTTPException(status_code=409, detail=f"The object with isbn={book_db.isbn} is already exists")
    keys_list = list(books_db.keys())
    for i in range(0, len(keys_list)):
        if i < len(keys_list)-1:
            if keys_list[i+1] - keys_list[i] != 1:
                books_db[keys_list[i]+1] = book
                return Response(status_code=201)
        else:
            books_db[keys_list[i]+1] = book
            return Response(status_code=201)


@router.get("/books/", response_model=list[Book])
async def get_book_list(
        author: Optional[str] = Query(default=None, min_length=3),
        year: Optional[PositiveInt] = Query(default=None, gt=1800, lt=2025),
):
    if author and year is None:
        books_list = list()
        for book in books_db.values():
            if book.author == author:
                books_list.append(book)
        return books_list
    elif year and author is None:
        books_list = list()
        for book in books_db.values():
            if book.year == year:
                books_list.append(book)
        return books_list
    elif author and year:
        books_list = list()
        for book in books_db.values():
            if book.author == author and book.year == year:
                books_list.append(book)
        return books_list
    else:
        return list(books_db.values())


@router.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: Annotated[int, Path(ge=0)]):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    return book


@router.put("/books/{book_id}")
async def put_book_by_id(
        book_id: Annotated[int, Path(ge=0)],
        new_book: Book
):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    books_db[book_id] = new_book
    return Response(status_code=200)


@router.patch("/books/{book_id}")
async def patch_book(
        book_id: Annotated[int, Path(ge=0)],
        book_patched: BookToPatch
):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    if book_patched.title:
        book.title = book_patched.title
    if book_patched.author:
            book.author = book_patched.author
    if book_patched.year:
        book.year = book_patched.year
    if book_patched.isbn:
        book.isbn = book_patched.isbn
    books_db[book_id] = book
    return Response(status_code=200)


@router.delete("/books/{book_id}")
async def delete_book_by_id(book_id: Annotated[int, Path(ge=0)]):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    del books_db[book_id]
    return Response(status_code=200)