# 使用官方 Python 映像作為基礎映像
FROM python:3.12.4-slim

# 設定工作目錄
WORKDIR /app

# 安裝 Poetry
RUN pip install poetry

# 將 pyproject.toml 和 poetry.lock 文件複製到工作目錄
COPY pyproject.toml poetry.lock ./

# 安裝依賴項
RUN poetry install --no-root

# 將應用程式代碼複製到工作目錄
COPY . .

# 設置環境變量
ENV FLASK_APP=your_package/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# 開放應用程式執行的端口
EXPOSE 5000

# 執行應用程式
CMD ["poetry", "run", "flask", "run"]
