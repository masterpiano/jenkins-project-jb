FROM python:3.11-slim
WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./rpt-project
WORKDIR ./rpt-project


COPY ./app.py .

EXPOSE 80
CMD ["python","app.py"]