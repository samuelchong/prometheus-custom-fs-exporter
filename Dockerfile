FROM python:3.8
COPY requirements.txt /opt/app/requirements.txt
COPY prometheus-custom-fs-exporter.py /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
CMD ["python", "/opt/app/prometheus-custom-fs-exporter.py"]