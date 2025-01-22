FROM python:3.12

RUN mkdir /doc

WORKDIR /doc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /doc/docker_scripts/*.sh

#RUN apt-get update && apt-get install -y \
#    tesseract-ocr \
#    libtesseract-dev \
#    tesseract-ocr-rus \
#    && apt-get clean

# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

