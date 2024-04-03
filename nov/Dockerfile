FROM python:3.10

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install bootstrap5
RUN pip install django-bootstrap-v5

# Copy the current directory contents into the app directory
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Set the command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]