from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import TEXT
from datetime import date

class Base(DeclarativeBase): ...

class BookRow(Base):
    __tablename__ = 'books'

    id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    acquired_at: Mapped[date] = mapped_column(nullable=False)

