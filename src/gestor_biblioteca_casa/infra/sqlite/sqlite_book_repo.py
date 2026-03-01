from pathlib import Path
from uuid import UUID
import sqlite3
from typing import Callable
from datetime import date

from gestor_biblioteca_casa.domain.models import Book
from gestor_biblioteca_casa.ports.book_contract import BookRepo
from gestor_biblioteca_casa.infra.errors import BookAlreadyExists

ConnectionFactory = Callable[[], sqlite3.Connection] # para typing, definimos el factory

class SQLiteBookRepository(BookRepo):
    def __init__(self, connection_factory=Callable[[], sqlite3.Connection]) -> None:
        self._get_connection = connection_factory

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        data = dict(row)
        data['id'] = UUID(data['id'])
        data['acquired_at'] = date.fromisoformat(data['acquired_at'])
        return Book(**data)

    def add(self, book: Book) -> UUID:
        stmt = '''
        INSERT INTO books (id, title, author, acquired_at)
        VALUES (?, ?, ?, ?)
        '''
        values = (book.id.hex, book.title, book.author, book.acquired_at.isoformat())
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute(stmt, values)
            return book.id
        except sqlite3.IntegrityError:
            raise BookAlreadyExists(f'Book already exists with id: {book.id}.')

    def list(self, limit: int, offset: int) -> list[Book]:
        stmt = '''
        SELECT * 
        FROM books
        ORDER BY id
        LIMIT ?
        OFFSET ?'''
        values = (limit, offset)
        with self._get_connection() as conn:
            cur = conn.cursor()
            
            rows = cur.execute(stmt, values).fetchall()

        return [self._row_to_book(row) for row in rows]