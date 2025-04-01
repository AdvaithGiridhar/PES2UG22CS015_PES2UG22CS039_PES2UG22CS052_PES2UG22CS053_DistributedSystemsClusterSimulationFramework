FROM python:3.8

WORKDIR /app

COPY node.py .

RUN pip install requests

CMD ["python", "node.py"]
