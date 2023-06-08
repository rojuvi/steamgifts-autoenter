FROM selenium/standalone-chrome:113.0

WORKDIR /app
COPY *.py /app/
COPY requirements.txt /app/
COPY docker_entrypoint.sh /app/
USER root
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN apt-get install google-chrome-stable
RUN pip install -r requirements.txt

CMD [ "bash", "docker_entrypoint.sh" ]