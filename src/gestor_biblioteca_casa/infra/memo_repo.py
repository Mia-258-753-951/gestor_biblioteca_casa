from uuid import UUID

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.domain.models import Book

class BookMemoRepository(BookRepo):

    def __init__(self) -> None:
        self.data = {}

    def add(self, book: Book) -> UUID:
        self.data[book.id] = book
        return book.id
    
    def list(self) -> list[Book]:
        return [b for b in self.data.values()]
