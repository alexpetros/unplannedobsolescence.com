.PHONY: dev
dev:
	zola serve

.PHONY: build
build:
	zola build

.PHONY: deploy
deploy: build
	rsync -r --delete ./public mrg:/var/www/unplannedobsolescence.com

.PHONY: clean
clean:
	rm -rf public
