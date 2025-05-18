# This is the first instruction in almost every Dockerfile. It sets the base image for the build process. 
# It gets official Docker image for Python from Docker Hub of version 3.11 with minimal base image .
FROM python:3.11-slim

# This setting up a new user (so we don't run stuff as root user for safety)
RUN groupadd -r usergroup && useradd -r -g usergroup vaishnavee

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file from local machine into the current working directory to install Python packages.
COPY requirements.txt .

# Install all the Python packages we need, without caching to keep it light.
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the source code and files into the container 
COPY src/ .
COPY . .

# Give ownership of everything in /app to our non-root user
RUN chown -R vaishnavee:usergroup /app

# Switch to our safer, non-root user for running the app
USER vaishnavee

# Open up port 5000 (it is the port our Flask app will run on)
EXPOSE 5000

# Finally, run the app using plain Python
CMD ["python", "app.py"]
