FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# El frontend correrá en el puerto 5000
CMD ["python", "run.py"]
