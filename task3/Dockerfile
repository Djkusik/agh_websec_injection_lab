FROM vulhub/django:2.2.3

COPY src/ /usr/src/
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV ADMIN_PASS admin123 

WORKDIR /usr/src
ENTRYPOINT [ "/docker-entrypoint.sh"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:5002" ]