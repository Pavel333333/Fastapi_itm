from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Добавление CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:8000"],  # Разрешаем запросы только с этого домена (порт Django)
#     allow_credentials=True,
#     allow_methods=["*"],  # Разрешаем все HTTP методы
#     allow_headers=["*"],  # Разрешаем все заголовки
# )

app.include_router(router)


if '__name__' == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)