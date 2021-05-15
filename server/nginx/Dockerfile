# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

ENV FLASK_APP2=172.26.131.72

ENV FLASK_APP2=172.26.131.73

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/
