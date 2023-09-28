FROM public.ecr.aws/docker/library/python:3.9.13-slim-buster

RUN apt -y update && apt -y install curl wget zip

COPY push_repository.sh /push_repository.sh

ENTRYPOINT ["/push_repository.sh"]