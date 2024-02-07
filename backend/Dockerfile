FROM python:3.11.7-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]