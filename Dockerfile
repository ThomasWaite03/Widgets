FROM python:3
COPY src src 
WORKDIR /src
RUN pip install --no-cache-dir boto3
CMD ["python", "consumer.py", "-rq", "cs5260-requests", "-wt", "widgets"]
