# syntax=docker/dockerfile:1
FROM python:3.8-alpine
ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt
# Install virtual dependencies for pip install.
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
# Remove virtual dependencies
RUN apk del .tmp

# Copy resources across into container.
RUN mkdir /app
COPY ./* /app
WORKDIR /app
COPY ./scripts /scripts

# Give run permissions to scripts.
RUN chmod +x /scripts/*

# Create dirs for static files.
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Create a user with less privileges that root user.
# In case of container breach.
RUN adduser -D user
# Set owner of vol directory to the user so app has permissions to access it.
RUN chown -R user:user /vol
# 755 = user has full access.
RUN chmod -R 755 /vol/web
# Switch to new smaller user.
USER user

# Will boot up application.
CMD ["entrypoint.sh"]