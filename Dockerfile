FROM python:3.7.5-stretch
COPY . .
RUN  pip install -r requirements.txt
CMD python api.py
