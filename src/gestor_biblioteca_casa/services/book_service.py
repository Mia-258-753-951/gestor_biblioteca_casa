from uuid import uuid4, UUID
from datetime import date

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.domain.models import Book

def create_book(repo: BookRepo, title: str, author: str, acquire_at: date) -> UUID:
    fake_id = uuid4()
    book = Book(id=fake_id, title= title, author= author, acquired_at=acquire_at)
    return repo.add(book)

def list_books(repo: BookRepo, size: int, page: int) -> list[Book]:
    if size < 1 or page <1:
        raise ValueError("'size' and 'page' must be >= 1.")
    
    limit = size
    offset = (page - 1) * size

    return repo.list(limit, offset)
