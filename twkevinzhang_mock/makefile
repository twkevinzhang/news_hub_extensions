# for python to print to stdout immediately
export PYTHONUNBUFFERED := 1

# for unittest
export PYTHONPATH := .:twkevinzhang_mock

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
	curl -sL https://raw.githubusercontent.com/twkevinzhang/news_hub/dev/news_hub_protos/domain_models.proto -o twkevinzhang_mock/mock_domain_models.proto
	curl -sL https://raw.githubusercontent.com/twkevinzhang/news_hub/dev/news_hub_protos/sidecar_api.proto -o twkevinzhang_mock/mock_api.proto
	sed -i '' 's/package news_hub.domain;/package twkevinzhang_mock.domain;/g' twkevinzhang_mock/mock_domain_models.proto
	sed -i '' 's/package news_hub.sidecar;/package twkevinzhang_mock.sidecar;/g' twkevinzhang_mock/mock_api.proto
	sed -i '' 's/import "domain_models.proto";/import "mock_domain_models.proto";/g' twkevinzhang_mock/mock_api.proto
	sed -i '' 's/news_hub.domain./twkevinzhang_mock.domain./g' twkevinzhang_mock/mock_api.proto
	python -m grpc_tools.protoc -Itwkevinzhang_mock --python_out=twkevinzhang_mock --pyi_out=twkevinzhang_mock --grpc_python_out=twkevinzhang_mock twkevinzhang_mock/*.proto
	sed -i '' 's/import mock_domain_models_pb2/from . import mock_domain_models_pb2/g' twkevinzhang_mock/mock_api_pb2.py
	sed -i '' 's/import mock_api_pb2/from . import mock_api_pb2/g' twkevinzhang_mock/mock_api_pb2_grpc.py
	sed -i '' 's/import mock_domain_models_pb2/from . import mock_domain_models_pb2/g' twkevinzhang_mock/mock_api_pb2_grpc.py
