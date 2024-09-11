FROM python:3.9-slim

WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the PORT environment variable
ENV PORT=8080

# Use CMD instead of ENTRYPOINT for more flexibility
CMD ["python", "app.py"]