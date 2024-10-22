from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt


class Book(BaseModel):
    title: str
    author: str
    year: PositiveInt | None
    isbn: str


books_db = dict([
    (0, Book(title='New Mexico', author='JessePinkman', year=2004, isbn='13579')),
    (1, Book(title='AmazingMe', author='MikeTheKiller', year=2004, isbn='24680')),
    (2, Book(title='Super Thinker', author='JessePinkman', year=2015, isbn='11223'))
])


app = FastAPI()


@app.post("/books/")
async def create_book(book: Book):
    current_amount_of_keys = 0
    for book_db in books_db.values():
        current_amount_of_keys += 1
        if book_db.isbn == book.isbn:
            break
    books_db[current_amount_of_keys] = book
    return book

@app.get("/books/")
async def get_all():
    for book_bd in books_db.values():
        yield book_bd