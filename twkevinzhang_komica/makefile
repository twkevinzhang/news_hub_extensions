# for python to print to stdout immediately
export PYTHONUNBUFFERED := 1

# for unittest
export PYTHONPATH := .:twkevinzhang_komica

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
	python -m grpc_tools.protoc -Itwkevinzhang_komica --python_out=twkevinzhang_komica --pyi_out=twkevinzhang_komica --grpc_python_out=twkevinzhang_komica twkevinzhang_komica/*.proto
