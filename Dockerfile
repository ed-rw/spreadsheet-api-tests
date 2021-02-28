FROM python:3.8-alpine

COPY tests/ /opt/tests
COPY entrypoint.sh /opt/entrypoint.sh

WORKDIR /opt/tests

RUN chmod +x /opt/entrypoint.sh && \
    pip install pipenv && \
    pipenv install

ENTRYPOINT ["/opt/entrypoint.sh"]
