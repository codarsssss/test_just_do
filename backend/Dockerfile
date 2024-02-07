FROM python:3.11.7
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["daphne", "foodgram.wsgi:application", "--bind", "0:8000", "--reload"]