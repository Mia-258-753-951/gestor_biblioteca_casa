from fastapi import APIRouter
from gestor_biblioteca_casa.services.book_service import create_book, list_books
from gestor_biblioteca_casa.infra.memo_repo import BookMemoRepository

router = APIRouter(prefix='/books', tags=['Books'])

repo = BookMemoRepository()

@router.post('/')
def new_book(title: str, author: str):
    new_id = create_book(repo, title, author)

    return {'id': new_id}

@router.get('/')
def list_all_books():
    return list_books(repo)
