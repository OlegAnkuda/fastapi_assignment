from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, PositiveInt, Field
from fastapi.exceptions import HTTPException


class Book(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    year: Optional[PositiveInt] = Field(default=None, gt=1800, lt=2025)
    isbn: str = Field()


class Book_to_patch(Book):
    title: Optional[str] = Field(default=None, min_length=3)
    author: Optional[str] = Field(default=None, min_length=3)
    isbn: Optional[str] = Field(default=None)


# Default dict filling
books_db = dict([
    (0, Book(title='New Mexico', author='JessePinkman', year=2004, isbn='13579')),
    (1, Book(title='AmazingMe', author='MikeTheKiller', year=2004, isbn='24680')),
    (2, Book(title='Super Thinker', author='JessePinkman', year=2015, isbn='11223'))
])


app = FastAPI()


@app.post("/books/")
async def post_book(book: Book):
    for book_db in books_db.values():
         if book_db.isbn == book.isbn:
             raise HTTPException(status_code=409, detail=f"The object with isbn={book_db.isbn} is already exists")
    keys_list = list(books_db.keys())
    for i in range(0, len(keys_list)):
        if i < len(keys_list)-1:
            if keys_list[i+1] - keys_list[i] != 1:
                books_db[keys_list[i]+1] = book
                raise HTTPException(status_code=201)
        else:
            books_db[keys_list[i]+1] = book
            raise HTTPException(status_code=201)


@app.get("/books/", response_model=list[Book])
async def get_book_list(
        author: Optional[str] = Query(default=None, min_length=3),
        year: Optional[PositiveInt] = Query(default=None, gt=1800, lt=2025),
):
    if author and year == None:
        books_list = list()
        for book in books_db.values():
            if book.author == author:
                books_list.append(book)
        return books_list
    elif year and author == None:
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


@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    return book


@app.put("/books/{book_id}")
async def put_book_by_id(book_id: int, new_book: Book):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    books_db[book_id] = new_book
    raise HTTPException(status_code=200)


@app.patch("/books/{book_id}")
async def patch_book(book_id: int, book_patched: Book_to_patch):
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
    raise HTTPException(status_code=200)


@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404)
    del books_db[book_id]
    raise HTTPException(status_code=200)