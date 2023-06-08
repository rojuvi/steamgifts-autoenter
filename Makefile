-include .env
export
VERSION=$(shell cat VERSION)
IMAGE_NAME=rojuvi/steamgifts-autoenter

run:
	echo ${VERSION}
	if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
	.venv/bin/pip install -r requirements.txt
	.venv/bin/python src/main.py

build:
	docker build . -t ${IMAGE_NAME}:${VERSION}
	docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest

publish:
	docker push ${IMAGE_NAME}:${VERSION}
	docker push ${IMAGE_NAME}:latest