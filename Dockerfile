FROM python:3.12-slim

# Chromium + matching chromedriver from Debian, plus CJK fonts so Korean
# pages render properly in screenshots.
RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium chromium-driver fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY collect_coins.py .

ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    HEADLESS=true \
    CHROME_PROFILE_DIR=/profile \
    PYTHONUNBUFFERED=1

CMD ["python", "collect_coins.py"]
