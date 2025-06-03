dev:
	zola serve

build:
	zola build

deploy: build
	rsync -r --delete ./public mrg:/var/www/unplannedobsolescence.com

clean:
	rm -rf public
