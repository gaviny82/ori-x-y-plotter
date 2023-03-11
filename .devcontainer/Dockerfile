FROM ubuntu:latest

USER root

# Install Python 3.9
RUN apt-get update && \
    apt-get install -y python3.9 python3-pip git

# Install Python packages
COPY requirements.txt /tmp/pip-tmp/
RUN pip install update && \
    pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt

# Clean up
RUN rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/pip-tmp