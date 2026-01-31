#!/bin/bash

IMAGE_NAME="html-to-markdown:v1.0"
DOCKERFILE_PATH="."
CONTAINER_NAME="html-to-markdown-container"

# 1. Check if image exists
if [ -z "$(docker images -q $IMAGE_NAME 2>/dev/null)" ]; then
    echo "🔍 镜像 $IMAGE_NAME 不存在，准备开始构建..."
    
    # 2. Build image
    docker build -t $IMAGE_NAME $DOCKERFILE_PATH
    
    if [ $? -eq 0 ]; then
        echo "✅ 镜像构建成功！"
    else
        echo "❌ 镜像构建失败，请检查 Dockerfile。"
        exit 1
    fi
else
    echo "🚀 镜像 $IMAGE_NAME 已存在，跳过构建步骤。"
fi

# 4. Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "🚀 容器 $CONTAINER_NAME 不存在，正在创建并启动..."
    
    # Create temp_data folder if it doesn't exist
    mkdir -p temp_data
    
    # Run container with mounts
    docker run --name $CONTAINER_NAME \
        -v $(pwd)/html-to-markdown.ts:/app/html-to-markdown.ts \
        -v $(pwd)/convert.ts:/app/convert.ts \
        -v $(pwd)/temp_data:/app/temp_data \
        -d $IMAGE_NAME
else
    echo "✅ 容器 $CONTAINER_NAME 已存在。"

    # 5. Check if container is running
    RUNNING=$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)

    if [ "$RUNNING" != "true" ]; then
        echo "⏳ 容器已停止，正在启动..."
        docker start $CONTAINER_NAME
        echo "✅ 容器已启动。"
    else
        echo "🔥 容器正在运行中。"
    fi
fi
