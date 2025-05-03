# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file if you have one (optional)
# ADD requirements.txt /app/

# Install necessary Python libraries
RUN pip install requests
RUN pip install schedule
RUN pip install pyyaml
RUN apt-get update && apt-get install -y --no-install-recommends curl

# Copy the weather_ingestion.py script into the container
COPY weather_ingestion.py /app/

# Define the entry point command to run the Python script
CMD ["python", "weather_ingestion.py"]
