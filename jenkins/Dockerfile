FROM jenkins/jenkins:lts
USER root

RUN apt-get update && apt-get install -y curl python3-venv

RUN curl -LO "https://dl.k8s.io/release/v1.31.0/bin/linux/$(dpkg --print-architecture)/kubectl" && \
    install kubectl /usr/local/bin/ && rm kubectl

RUN curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

RUN python3 -m venv /opt/sast && \
    /opt/sast/bin/pip install ansible-lint checkov

ENV PATH="/opt/sast/bin:${PATH}"
USER jenkins