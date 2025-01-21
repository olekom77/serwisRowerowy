FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Run the application
CMD python main.py