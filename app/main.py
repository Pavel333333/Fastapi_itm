from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()

app.include_router(router)


if '__name__' == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)