.PHONY: help install serve build clean markdown-pack

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv venv
	@echo "Run 'source .venv/bin/activate' to activate the virtual environment"
	. .venv/bin/activate && uv pip install -e .

serve: ## Serve docs locally
	mkdocs serve -s

build: ## Build the documentation
	mkdocs build -s

clean: ## Clean build artifacts
	rm -rf site/ _multirepo/ .cache/

markdown-pack: ## Create a markdown pack of all docs for MCP ingestion
	@echo "Creating markdown pack by fetching from source repos..."
	@if [ -f .venv/bin/activate ]; then \
		. .venv/bin/activate && python fetch_markdown_pack.py; \
	else \
		python3 fetch_markdown_pack.py; \
	fi
	@echo "Pack created in markdown-pack/"

pack: markdown-pack ## Alias for markdown-pack