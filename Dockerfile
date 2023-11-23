FROM python:3.10

WORKDIR /home


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./ /home/
RUN useradd -ms /bin/bash admin
RUN chown -R admin:admin /home/
RUN mkdir /home/db
RUN chmod -R 777 /home/db
RUN mv /home/database.db /home/db/database.db
RUN pip install -r /home/requirements.txt && apt-get update && apt-get install sqlite3
USER admin
ENV PYTHONPATH /home/
ENV PATH=$PATH:/home/

ENTRYPOINT ["python", "main.py"]

