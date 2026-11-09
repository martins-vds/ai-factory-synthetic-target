TAILWIND_VERSION := 4.1.13
TAILWIND_CLI ?= $(HOME)/.local/bin/tailwindcss
TAILWIND_URL := https://github.com/tailwindlabs/tailwindcss/releases/download/v$(TAILWIND_VERSION)/tailwindcss-linux-x64

.PHONY: run tailwind-install tailwind-build

run:
	python manage.py runserver "0.0.0.0:$${PORT:-8080}"

tailwind-install:
	mkdir -p "$(dir $(TAILWIND_CLI))"
	curl -fsSL "$(TAILWIND_URL)" -o "$(TAILWIND_CLI)"
	chmod +x "$(TAILWIND_CLI)"

tailwind-build:
	@set -eu; mkdir -p static/css; input=$$(mktemp static/css/.tailwind-input.XXXXXX.css); \
	trap 'rm -f "$$input"' EXIT; \
	printf '@import "tailwindcss" source(none);\n@source "../../templates";\n' > "$$input"; \
	"$(TAILWIND_CLI)" -i "$$input" -o static/css/tailwind.css
