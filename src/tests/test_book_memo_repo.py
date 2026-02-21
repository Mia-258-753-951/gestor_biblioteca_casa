from uuid import uuid4

from gestor_biblioteca_casa.domain.models import Book
from gestor_biblioteca_casa.infra.memo_repo import BookMemoRepository

def test_add_persist_in_memory_and_list_returns_in_memory_books():
    repo = BookMemoRepository()
    fake_id = uuid4()
    book = Book(id= fake_id, title='titulo1', author='autor1')

    new_id = repo.add(book)

    assert new_id == fake_id
    assert repo.data[fake_id] == book
    assert repo.list() == [book]


    