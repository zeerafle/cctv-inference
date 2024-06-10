install:
	pip install --upgrade pip &&\
		pip install black pylama

lint:
	black .
	pylama .
