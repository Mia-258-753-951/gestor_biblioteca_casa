from fastapi import FastAPI
from gestor_biblioteca_casa.entrypoints.api.routers import books


app = FastAPI()
app.include_router(books.router)

@app.get('/health')
def health():
    return {'status': 'ok'}