# for python to print to stdout immediately
export PYTHONUNBUFFERED := 1

# for unittest
export PYTHONPATH := .

.PHONY: install
install:
	pip install grpcio-tools===1.67.1
	pip install -r requirements.txt

.PHONY: clean
clean:
	pip freeze | xargs pip uninstall -y

.PHONY: test
test:
	python -m unittest discover test

.PHONY: run
run:
	python test_resolver_impl.py

.PHONY: proto
proto:
	rm -rf news_hub_protos
	npx -y degit twkevinzhang/news_hub/news_hub_protos#dev news_hub_protos --force
	python -m grpc_tools.protoc -Inews_hub_protos --python_out=twkevinzhang_mock --pyi_out=twkevinzhang_mock --grpc_python_out=twkevinzhang_mock news_hub_protos/*.proto
