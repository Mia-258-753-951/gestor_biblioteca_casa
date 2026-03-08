from uuid import UUID
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.domain.models import Book
from gestor_biblioteca_casa.infra.sqlalchemy.models import BookRow
from gestor_biblioteca_casa.infra.errors import BookAlreadyExists 

class SQLAlchemyBookRepository(BookRepo):

    def __init__(self, factory: sessionmaker) -> None:
        self.factory = factory

    def _book_to_row(self, book: Book) -> BookRow:
        return BookRow(
            id=book.id.hex,
            title=book.title,
            author=book.author,
            acquired_at= book.acquired_at,
        )
    
    def _row_to_book(self, row: BookRow) -> Book:
        return Book(
            id=UUID(row.id),
            title=row.title,
            author=row.author,
            acquired_at=row.acquired_at,
        )

    def add(self, book: Book) -> UUID:
        try:
            with self.factory() as s:
                s.add(self._book_to_row(book))
                s.commit()
            return book.id
        except IntegrityError:
            raise BookAlreadyExists(f'Book already exists with id: {book.id}.')

    def list(self, limit: int, offset: int) -> list[Book]:
        stmt = (
                select(BookRow).
                order_by(BookRow.id).
                limit(limit).
                offset(offset)
            )
        with self.factory() as s:            
            rows = s.scalars(stmt).all()

            return [self._row_to_book(row) for row in rows]