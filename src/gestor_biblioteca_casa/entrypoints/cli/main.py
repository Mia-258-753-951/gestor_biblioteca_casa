import typer

from gestor_biblioteca_casa.entrypoints.cli import books
from gestor_biblioteca_casa.bootstrap import get_book_repo

def create_app(get_book_repo_fn = get_book_repo) -> typer.Typer:
    app = typer.Typer()

    books_app = books.create_app(get_repo=get_book_repo_fn)
    app.add_typer(books_app, name='books')

    return app
app = create_app()



