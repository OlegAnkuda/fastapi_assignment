from src.schemas import Book


books_db = dict([
    (0, Book(title='New Mexico', author='JessePinkman', year=2004, isbn='13579')),
    (1, Book(title='AmazingMe', author='MikeTheKiller', year=2004, isbn='24680')),
    (2, Book(title='Super Thinker', author='JessePinkman', year=2015, isbn='11223'))
])