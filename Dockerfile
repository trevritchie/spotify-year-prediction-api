# Use Python 3.11 slim image
FROM python:3.11-slim

# Create user with ID 1000
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Copy requirements with user ownership
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application files with user ownership
COPY --chown=user app/ ./app/
COPY --chown=user models/ ./models/
COPY --chown=user static/ ./static/

# Switch to non-root user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expose port 8000
EXPOSE 8000

# Run application on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
