FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install pip and any dependencies (modify if you add requirements.txt later)
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run your parser script
CMD ["python", "ediParser.py"]