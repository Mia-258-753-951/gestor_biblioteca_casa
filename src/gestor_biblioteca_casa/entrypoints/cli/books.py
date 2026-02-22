import typer
from rich.console import Console
from rich.table import Table

from gestor_biblioteca_casa.bootstrap import get_book_repo
from gestor_biblioteca_casa.services.book_service import create_book, list_books

console = Console()
app = typer.Typer()

repo = get_book_repo()

@app.command()
def new_book(
    title: str = typer.Argument(...),
    author: str = typer.Option('Anónimo', '--autor', '-a')  # Por defecto anónimo si no se facilita autor
):
    added_id = create_book(repo, title, author)

    typer.echo(f'Libro guardado con id: {added_id}.')

@app.command()
def show_books(
    size: int = typer.Option(20, '--size', '-s'),
    page: int = typer.Option(1, '--page', '-p')
):
    books = list_books(repo, size, page)

    if not books:
        console.print('No hay libros guardados.')
        return

    table = Table(title='Libros')

    table.add_column('ID')
    table.add_column('Título')
    table.add_column('Autor')
    
    for book in books:
        table.add_row(book.id.hex, book.title, book.author)
    console.print(table)


