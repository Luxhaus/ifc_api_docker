FROM python:3.9

# Set working directory
WORKDIR /code

# Copy and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Create the temp directory within the app folder
RUN mkdir -p /code/app/temp

# Expose port 80 and run the application
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host",  "0.0.0.0", "--port", "80"]