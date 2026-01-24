FROM python:3.12-slim

WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Postgres client for wait-for-postgres.sh
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Make wait script executable
RUN chmod +x wait-for-postgres.sh

# Environment variable for Flask
ENV FLASK_ENV=development
ENV FLASK_APP=run.py

# Command to run the app
CMD ["./wait-for-postgres.sh", "db", "python", "run.py"]