FROM python:3.11
FROM java:8
COPY app /app
WORKDIR /app
RUN apt-get update 
RUN apt-get -y install tesseract-ocr
RUN apt-get -y install libmagic1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.download punkt
RUN python -m spacy download en_core_web_sm
CMD ["python", "crawler.py"]