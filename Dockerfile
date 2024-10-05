FROM python:3-alpine

ENV VIRTUAL_ENV=/home/exporter/venv

WORKDIR /tasmota_exporter
COPY . .

RUN chmod +rx export.py

RUN addgroup -S exporter && adduser -S exporter -G exporter
USER exporter

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt
EXPOSE 8226
CMD ["python", "export.py"]
