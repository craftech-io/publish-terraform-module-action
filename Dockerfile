FROM public.ecr.aws/docker/library/python:3.9.13-slim-buster

RUN apt -y update && apt -y install curl \
    && pip install awscli \
    && curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash \

COPY push_repository.sh /usr/local/bin/push_repository

CMD push_repository