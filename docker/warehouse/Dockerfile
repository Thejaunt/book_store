FROM python:3.11-slim as python-base

RUN apt-get update --fix-missing && apt-get upgrade -qy

RUN apt update && apt install curl -y

FROM python-base as python-compile

COPY ./warehouse/requirements.txt .

RUN pip install --no-cache-dir -t /python -r requirements.txt

FROM python-base as hillel_example

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY --from=python-compile /python /home/appuser/python
ENV PYTHONPATH=/home/appuser/python
ENV PATH="${PYTHONPATH}/bin:${PATH}"

COPY ./warehouse /home/appuser/app
COPY ./docker/warehouse /home/appuser/app/docker
WORKDIR /home/appuser/app

RUN chmod +x docker/runserver.sh docker/wait-for-command.sh docker/docker-entrypoint.sh

EXPOSE 8002

ENTRYPOINT ["/bin/bash", "docker/docker-entrypoint.sh"]
CMD ["python", "main.py", "runserver"]