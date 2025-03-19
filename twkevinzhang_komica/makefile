# for python to print to stdout immediately
export PYTHONUNBUFFERED := 1

# for unittest
export PYTHONPATH := src

.PHONY: install
install:
	pip install grpcio-tools===1.67.1
	pip install -r src/requirements.txt

.PHONY: clean
clean:
	pip freeze | xargs pip uninstall -y

.PHONY: proto
proto:
	python -m grpc_tools.protoc -I../news_hub_protos --python_out=src --pyi_out=src --grpc_python_out=src ../news_hub_protos/*.proto

.PHONY: test
test:
	python -m unittest discover test

.PHONY: run
run:
	python src/main.py
