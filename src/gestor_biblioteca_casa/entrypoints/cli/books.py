import typer
from rich.console import Console
from rich.table import Table
from datetime import date
from collections.abc import Callable

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.services.book_service import create_book, list_books

GetRepo = Callable[[], BookRepo]

def default_get_repo() -> BookRepo:
    # Import lazy: evita tocar bootstrap al importar la app CLI
    from gestor_biblioteca_casa.bootstrap import get_book_repo
    return get_book_repo()

# definimos una función fábrica, construye y devuelve una app Typer
def create_app(get_repo: GetRepo=default_get_repo) -> typer.Typer:
    console = Console()
    app = typer.Typer()

    # la función callback se ejecuta antes de los command y define el 
    # contexto común de la app. Aquí guardamos la función get_repo 
    @app.callback()
    def main(ctx: typer.Context):
        ctx.obj = {'get_repo': get_repo}

    @app.command()
    def new_book(
        ctx: typer.Context,
        title: str = typer.Argument(...),
        insert_date: str = typer.Argument(..., help='isoformat: "YYYY-mm-dd"'),
        author: str = typer.Option('Anónimo', '--autor', '-a')  # Por defecto anónimo si no se facilita autor
    ):
        repo = ctx.obj['get_repo']()
        acquired_at = date.fromisoformat(insert_date)
        added_id = create_book(repo, title, author, acquired_at)

        typer.echo(f'Libro guardado con id: {added_id}.')

    @app.command()
    def show_books(
        ctx: typer.Context,
        size: int = typer.Option(20, '--size', '-s'),
        page: int = typer.Option(1, '--page', '-p')
    ):  
        repo = ctx.obj['get_repo']()
        books = list_books(repo, size, page)

        if not books:
            console.print('No books to show.')
            return

        table = Table(title='Libros')

        table.add_column('ID')
        table.add_column('Título')
        table.add_column('Autor')
        table.add_column('Fecha Adquisición')
        
        for book in books:
            table.add_row(book.id.hex, book.title, book.author, book.acquired_at.isoformat())
        console.print(table)

    return app
