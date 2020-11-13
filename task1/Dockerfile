FROM python:3.7-buster

RUN useradd tower

WORKDIR /home/tower

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en

COPY __init__.py run.py shell.py .en[v] ./
COPY app app

RUN chown -R tower:tower ./
USER tower

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]