FROM python:3.7

### environment
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
ENV STATIC_INDEX 0

ENV HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/

COPY flaskApp /app
COPY requirements.txt /app
COPY . /app

RUN mkdir /app/config

WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the start script provided by the parent image tiangolo/uwsgi-nginx which in turn will start Nginx and uWSGI

#CMD ["./start.sh"]
CMD ["uwsgi", "uwsgi.ini"]
