FROM python:3.9
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /app
COPY src/ /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt
EXPOSE 5000
CMD ["flask", "run"]