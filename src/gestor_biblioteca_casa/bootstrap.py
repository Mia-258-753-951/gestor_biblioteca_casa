
from gestor_biblioteca_casa.infra.memo_repo import BookMemoRepository

_repo = BookMemoRepository()

def get_book_repo():
    return _repo