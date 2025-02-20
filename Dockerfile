# Stage 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Stage 2: Final stage
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

ENV PATH=/usr/local/bin:$PATH

CMD ["python", "gesture_painting.py"]
