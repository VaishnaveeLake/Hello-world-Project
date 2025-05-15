FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r usergroup && useradd -r -g usergroup vaishnavee

# Set environment variable to avoid interaction during install
ENV DEBIAN_FRONTEND=noninteractive

# Update all OS packages, especially vulnerable ones
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      python3 python3-pip perl-base zlib1g && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade setuptools to fixed version
RUN python3 -m pip install --upgrade pip setuptools==70.0.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY . .

# Change ownership of /app to the new user and group
RUN chown -R vaishnavee:usergroup /app

# Switch to the non-root user
USER vaishnavee

EXPOSE 5000
CMD ["python", "app.py"]
