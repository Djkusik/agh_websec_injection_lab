FROM python:buster

RUN useradd tower

WORKDIR /home/tower

RUN pip install -U pip setuptools wheel
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en

COPY __init__.py run.py shell.py ./
COPY app app
COPY flags flags

RUN chown -R tower:tower ./
USER tower

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]