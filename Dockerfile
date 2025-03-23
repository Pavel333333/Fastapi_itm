FROM python:3.12

#RUN mkdir /doc

#WORKDIR /doc

# Создаём пользователя и директорию
RUN useradd -m -d /home/pavel pavel
RUN mkdir -p /home/pavel/dev/fastapi_itm && chown -R pavel:pavel /home/pavel

# Копируем и устанавливаем зависимости как root
WORKDIR /home/pavel/dev/fastapi_itm
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# RUN chmod a+x /doc/docker_scripts/*.sh  # это команда Unix/Linux, которая изменяет права доступа к файлам и директориям
RUN chmod a+x /home/pavel/dev/fastapi_itm/docker_scripts/*.sh  # это команда Unix/Linux, которая изменяет права доступа к файлам и директориям

# Переключаемся на пользователя pavel
USER pavel

#RUN apt-get update && apt-get install -y \
#    tesseract-ocr \
#    libtesseract-dev \
#    tesseract-ocr-rus \
#    && apt-get clean

# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

