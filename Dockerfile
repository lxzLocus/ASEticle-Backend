# ベースイメージとして公式のPythonイメージを使用
FROM python:3.12.4

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストールするためのrequirements.txtをコピー
COPY requirements.txt .

# ライブラリのインストール
RUN apt-get update && apt-get install -y \
  libpq-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt
