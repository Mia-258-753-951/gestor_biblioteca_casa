from dataclasses import dataclass
from uuid import UUID
from datetime import date

@dataclass
class Book:
    id: UUID
    title: str
    author: str
    acquired_at: date