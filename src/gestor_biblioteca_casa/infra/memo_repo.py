from uuid import UUID
from itertools import islice

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.domain.models import Book

class BookMemoRepository(BookRepo):

    def __init__(self) -> None:
        self.data = {}

    def add(self, book: Book) -> UUID:
        self.data[book.id] = book
        return book.id
    
    def list(self, limit: int, offset: int) -> list[Book]:
        return list(islice(self.data.values(), offset, offset + limit)) 
