export SERIOUS_PYTHON_SITE_PACKAGES := $(PWD)/build/site-packages

app:
# 	currently for Android
	rm -rf build/site-packages
	rm -rf app/dist && mkdir -p app/dist
	dart run serious_python:main package app/src -p Android --requirements -r,app/src/requirements.txt --asset app/dist/twkevinzhang_komica.zip --verbose

.PHONY: app
