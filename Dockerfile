FROM python:latest

WORKDIR /workdir
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000
CMD ["python3", "winfin.py"]