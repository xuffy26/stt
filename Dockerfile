# Use Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for pydub)
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the port (use the same port your Flask app runs on)
ENV PORT=10000
EXPOSE 10000

# Start your app with gunicorn
CMD ["gunicorn", "stt:app", "--bind", "0.0.0.0:10000"]
