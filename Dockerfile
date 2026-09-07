FROM python:3.12-slim

WORKDIR /sleepapi

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONPATH=/sleepapi/app

COPY . .

RUN python app/notebooks/preprocessing.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]