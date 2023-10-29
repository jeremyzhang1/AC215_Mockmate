FROM python:3.9

WORKDIR /sourcefiles

COPY ./requirements.txt /sourcefiles/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /sourcefiles/requirements.txt

COPY ./app /sourcefiles/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]