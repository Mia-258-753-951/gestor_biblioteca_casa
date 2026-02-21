from uuid import uuid4, UUID

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.domain.models import Book

def create_book(repo: BookRepo, title: str, author: str) -> UUID:
    fake_id = uuid4()
    book = Book(id=fake_id, title= title, author= author)
    return repo.add(book)

def list_books(repo: BookRepo) -> list[Book]:
    return repo.list()
