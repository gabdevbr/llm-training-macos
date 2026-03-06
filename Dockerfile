FROM node:18-alpine

# Install Python and dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    build-base \
    git

WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make scripts executable
RUN chmod +x setup.sh

# Expose port for Ollama
EXPOSE 11434

# Default to Python (can override with CMD)
CMD ["python3", "train.py"]
