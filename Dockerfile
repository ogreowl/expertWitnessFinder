# Use the official Python image with minimal size
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the CSV file
COPY latest5.csv .

# Copy the rest of the application code to the container
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set environment variables for Google Cloud Run (if any are needed)
# ENV HUGGINGFACE_API_KEY your-api-key

# Run the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "finder:app"]