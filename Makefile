all: build

build:
	python -m urubu build

serve:
	cd _build; python -m urubu serve

clean:
	cd _build; rm -rf *
