FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r src/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]