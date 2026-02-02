#!/bin/bash

IMAGE_NAME="aggregate-news:v1.0"
DOCKERFILE_PATH="." # Dockerfile 所在的目录
CONTAINER_NAME="aggregate-news-container" # 你的容器名称

# 1. 检查镜像是否存在
# docker images -q 会只返回镜像 ID，如果镜像不存在则返回空
if [ -z "$(docker images -q $IMAGE_NAME 2>/dev/null)" ]; then
    echo "🔍 镜像 $IMAGE_NAME 不存在，准备开始构建..."
    
    # 2. 构建镜像
    docker build -t $IMAGE_NAME $DOCKERFILE_PATH
    
    # 检查构建是否成功
    if [ $? -eq 0 ]; then
        echo "✅ 镜像构建成功！"
    else
        echo "❌ 镜像构建失败，请检查 Dockerfile。"
        exit 1
    fi
else
    # 3. 存在则跳过
    echo "🚀 镜像 $IMAGE_NAME 已存在，跳过构建步骤。"
fi

# 4. 检查容器是否存在（无论运行还是停止）
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "🚀 容器 $CONTAINER_NAME 不存在，正在创建并启动..."
    mkdir -p temp_data
    docker run --init --name $CONTAINER_NAME -v $(pwd)/news_fetch.py:/app/news_fetch.py -v $(pwd)/temp_data:/app/temp_data -v $(pwd)/web_scrape.py:/app/web_scrape.py -d $IMAGE_NAME
else
    echo "✅ 容器 $CONTAINER_NAME 已存在。"

    # 5. 检查容器是否正在运行
    RUNNING=$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)

    if [ "$RUNNING" != "true" ]; then
        echo "⏳ 容器已停止，正在启动..."
        docker start $CONTAINER_NAME
        echo "✅ 容器已启动。"
    else
        echo "🔥 容器正在运行中。"
    fi
fi