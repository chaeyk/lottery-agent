FROM public.ecr.aws/docker/library/python:3.11.6-bookworm

RUN apt-get update && apt-get install -y chromium chromium-driver

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY *.py /app/

RUN echo -n "Build Date: $(date)" > welcome.txt

ENTRYPOINT ["python3", "main.py"]
