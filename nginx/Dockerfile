FROM nginx:alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY multi-container.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY public/ /usr/share/nginx/html/

# Expose port
EXPOSE 8077

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]