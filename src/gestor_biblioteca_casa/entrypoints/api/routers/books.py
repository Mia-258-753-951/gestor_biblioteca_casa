from fastapi import APIRouter, Depends
from datetime import date

from gestor_biblioteca_casa.services.book_service import create_book, list_books
from gestor_biblioteca_casa.bootstrap import get_book_repo
from gestor_biblioteca_casa.ports.book_contract import BookRepo

router = APIRouter(prefix='/books', tags=['Books'])

@router.post('/')
def new_book(title: str, author: str, acquired_at: date,  repo: BookRepo = Depends(get_book_repo)):
    new_id = create_book(repo, title, author, acquired_at)

    return {'id': new_id}

@router.get('/')
def list_all_books(
    size: int=20,
    page: int=1,
    repo: BookRepo = Depends(get_book_repo),
):
    return list_books(repo, size, page)
