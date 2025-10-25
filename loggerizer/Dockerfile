FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
ENV PATH="/uv:/uvx:/root/.local/bin:$PATH"
ADD . /app
WORKDIR /app
CMD ["tail", "-f", "/dev/null"]