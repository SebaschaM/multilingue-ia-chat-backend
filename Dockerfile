FROM postgres:13 AS db
FROM python:3.10-slim
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt-get purge -y --auto-remove gcc
EXPOSE 5000
CMD ["python", "run.py"]
