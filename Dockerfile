FROM python:3.9

ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

RUN python manage.py makemigrations chats
RUN python manage.py makemigrations accounts
RUN python manage.py makemigrations posts
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
