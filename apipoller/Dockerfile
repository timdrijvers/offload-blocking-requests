FROM python:3.7-slim

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ linux-libc-dev  \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc g++ linux-libc-dev

COPY poller.py .

EXPOSE 5500
CMD ["python", "./poller.py"]
