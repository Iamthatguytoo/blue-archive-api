FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

# System dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget curl gnupg ca-certificates \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

USER appuser

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright's Chromium browser
RUN python -m playwright install chromium

COPY --chown=appuser:appuser . .

EXPOSE 8000

ENV PATH="/home/appuser/.local/bin:$PATH"

CMD ["uvicorn", "blue_archive_characters_api:server", "--host", "0.0.0.0", "--port", "8000"]