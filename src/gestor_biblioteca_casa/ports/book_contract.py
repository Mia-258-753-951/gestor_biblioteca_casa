from typing import Protocol
from uuid import UUID

from gestor_biblioteca_casa.domain.models import Book
class BookRepo(Protocol):
     def add(self, book: Book) -> UUID: ...

     def list(self, limit: int, offset: int) -> list[Book]: ...
