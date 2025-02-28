FROM python:3.9-slim as whisper

# System dependencies for Whisper
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY whisper-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY whisper-api/app/ .

FROM nginx:alpine as nginx
# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY nginx/public/ /usr/share/nginx/html/

# Final stage
FROM nginx:alpine

# Copy from nginx build
COPY --from=nginx /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY --from=nginx /usr/share/nginx/html/ /usr/share/nginx/html/

# Copy from whisper build
COPY --from=whisper /app /whisper
COPY --from=whisper /root/.cache/whisper /root/.cache/whisper

# Expose port
EXPOSE 8077

# Start both services
CMD ["nginx", "-g", "daemon off;"]