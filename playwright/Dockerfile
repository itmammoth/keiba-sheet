FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

# uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN uv pip install --system --no-cache-dir -r requirements.txt

CMD ["bash"]
