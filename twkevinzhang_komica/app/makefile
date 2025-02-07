install:
	pip install grpcio-tools
	pip install -r src/requirements.txt

clean:
	pip freeze | xargs pip uninstall -y

proto:
	python -m grpc_tools.protoc -Inews_hub_protos --python_out=src --pyi_out=src news_hub_protos/*.proto

.PHONY: install proto clean
