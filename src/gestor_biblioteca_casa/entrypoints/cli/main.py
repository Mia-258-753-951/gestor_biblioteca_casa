import typer

from gestor_biblioteca_casa.entrypoints.cli import books

app = typer.Typer()

app.add_typer(books.app, name='books')



