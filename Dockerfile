FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r usergroup && useradd -r -g usergroup vaishnavee

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