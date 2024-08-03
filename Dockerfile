FROM python:3.9-slim-buster
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# install necessary opencv dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install\
    libgl1\
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
