FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libgbm-dev \
    chromium \
    chromium-driver

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/bin/chromedriver:${PATH}"

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run script on container start
CMD ["python", "scrape.py"]