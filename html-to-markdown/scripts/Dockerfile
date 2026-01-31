FROM node:20-slim

WORKDIR /app

# Install bun for faster TypeScript execution
RUN npm install -g bun

# Create necessary directories
RUN mkdir -p /app/temp_data

# Keep container running
CMD ["tail", "-f", "/dev/null"]