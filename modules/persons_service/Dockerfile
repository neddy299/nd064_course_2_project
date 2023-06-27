FROM python:3.8-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY modules/persons_service/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY modules/persons_service/ .
COPY protobufs/ .

CMD ["python", "main.py"]