# Use the official Nginx image from Docker Hub
FROM nginx:1.25-alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx.conf to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Placeholder for copying SSL certificates
# COPY ./certs/ /etc/nginx/certs/

# Expose ports 80 and 443
EXPOSE 80
EXPOSE 443
