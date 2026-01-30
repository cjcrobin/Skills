# 使用 Playwright 官方镜像
FROM mcr.microsoft.com/playwright/python:v1.57.0

WORKDIR /app
COPY ./pyproject.toml ./
COPY ./README.md ./

RUN pip install uv
RUN uv sync --no-install-project

CMD ["tail", "-f", "/dev/null"]