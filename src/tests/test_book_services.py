
from uuid import uuid4, UUID
from gestor_biblioteca_casa.services.book_service import create_book, list_books
from gestor_biblioteca_casa.infra.memo_repo import BookMemoRepository
from gestor_biblioteca_casa.domain.models import Book

def test_create_book_persists_in_repo_and_returns_id():
    repo = BookMemoRepository()
    id_ = create_book(repo, title='libro de prueba', author='yo mismo')

    assert isinstance(id_, UUID)
    assert list_books(repo, 20, 1) == [repo.data[id_]]

def test_list_returns_added_books():
    fake_id1 = uuid4()
    fake_id2 = uuid4()

    repo = BookMemoRepository()
    repo.data = {
        'fakeid1': Book(id=fake_id1, title='titulo1', author='author1'),
        'fakeid2': Book(id=fake_id2, title='titulo2', author='author2')
        }
    
    assert len(list_books(repo,20, 1)) == 2
    assert list_books(repo, 20, 1)[0] == repo.data['fakeid1']
    assert list_books(repo, 20, 1)[1] == repo.data['fakeid2']
