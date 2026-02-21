from typer.testing import CliRunner
runner = CliRunner()

from gestor_biblioteca_casa.entrypoints.cli.main import app

def test_create_new_book_persists_in_memory():

    result = runner.invoke(app, ['books', 'new-book', 'El Quijote', '--autor', 'Cervantes'])

    assert result.exit_code == 0
    assert 'Libro guardado con id:' in result.stdout


def test_list_show_stored_book():

    runner.invoke(app, ['books', 'new-book', 'Libro Prueba 1', '-a', 'prueba 1'])

    result = runner.invoke(app, ['books', 'show-books'])

    assert 'Libro Prueba 1' in result.stdout
