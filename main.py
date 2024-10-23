from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, PositiveInt, Field


class Book(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    year: PositiveInt | None = Field(gt=1800, lt=2025)
    isbn: str


# Default dict filling
books_db = dict([
    (0, Book(title='New Mexico', author='JessePinkman', year=2004, isbn='13579')),
    (1, Book(title='AmazingMe', author='MikeTheKiller', year=2004, isbn='24680')),
    (2, Book(title='Super Thinker', author='JessePinkman', year=2015, isbn='11223'))
])


app = FastAPI()


# Мне не нравится реализация, хочу потом переделать принцип получения id, чтобы заполнять пробелы по ключам в словаре.
@app.post("/books/")
async def post_book(book: Book):
    keys_list = list(books_db.keys())
    last_book_id = keys_list[-1]
    for book_db in books_db.values():
        if book_db.isbn == book.isbn:
            break # Need to throw exception

    books_db[last_book_id + 1] = book
    return book


# Нужен список или вывод поэлементно? С Query параметрами не нравится перебор условий,
# потом хочу придумать как переделать проще.
@app.get("/books/")
async def get_book_list(
        author: Annotated[
                    str | None, Query(min_length=3)
                ] = None,
        year: Annotated[
                    PositiveInt | None, Query(gt=1800, lt=2025)
                ] = None,
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


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    try:
        return books_db[book_id]
    except Exception:
        return 0 # Need to throw exception


# Надо обновлять по полям отдельно или обновлять всю информацию целиком?
@app.put("/books/{book_id}")
async def put_book_by_id(book_id: int, book: Book):
    try:
        books_db[book_id] = book
    except Exception:
        return 0 # Need to throw exception


@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    try:
        del books_db[book_id]
    except Exception:
        return 0  # Need to throw exception