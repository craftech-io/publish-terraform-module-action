FROM public.ecr.aws/docker/library/python:3.9.13-slim-buster

RUN apt -y update && apt -y install curl wget zip

COPY push_repository.sh /push_repository.sh
COPY requirements.txt /requirements.txt
COPY terraform_required_versions.py /terraform_required_versions.py

RUN chmod 111 /push_repository.sh
RUN pip install -r /requirements.txt

ENTRYPOINT ["/push_repository.sh"]