from fastapi import FastAPI

app = FastAPI()

@app.get('/health')
def hello():
    return {'status': 'ok'}