FROM python:3.8
LABEL maintainer "Anis Boudih anisboudih@gmail.com"

WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./

EXPOSE 4999
CMD ["python", "./run.py"]