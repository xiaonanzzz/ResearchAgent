.PHONY: help init list

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-18s %s\n", $$1, $$2}'

init: ## Initialize a new research project: make init research-xxx
	@if [ -z "$(filter-out init,$(MAKECMDGOALS))" ] && [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make init <project-name>"; \
		echo "Example: make init research-image-classification"; \
		exit 1; \
	fi
	@PROJECT_NAME=$(word 2,$(MAKECMDGOALS)); \
	if [ -d "$$PROJECT_NAME" ]; then \
		echo "Error: $$PROJECT_NAME already exists"; \
		exit 1; \
	fi; \
	echo "Initializing $$PROJECT_NAME..."; \
	mkdir -p $$PROJECT_NAME/.claude/commands; \
	mkdir -p $$PROJECT_NAME/.claude/rules; \
	mkdir -p $$PROJECT_NAME/data-protocols; \
	mkdir -p $$PROJECT_NAME/evaluation-protocols; \
	for f in skills/*.md; do \
		cp $$f $$PROJECT_NAME/.claude/commands/$$(basename $$f); \
		echo "  skill: $$f -> .claude/commands/$$(basename $$f)"; \
	done; \
	for f in rules/*.md; do \
		cp $$f $$PROJECT_NAME/.claude/rules/$$(basename $$f); \
		echo "  rule:  $$f -> .claude/rules/$$(basename $$f)"; \
	done; \
	cp templates/research-objective.template.md $$PROJECT_NAME/research-objective.md; \
	echo "  created: research-objective.md"; \
	cp templates/research-data.template.md $$PROJECT_NAME/research-data.md; \
	echo "  created: research-data.md"; \
	cp templates/data_protocol.template.py $$PROJECT_NAME/data-protocols/; \
	echo "  created: data-protocols/data_protocol.template.py"; \
	cp -r templates/evaluation-protocol-template $$PROJECT_NAME/evaluation-protocols/; \
	echo "  created: evaluation-protocols/evaluation-protocol-template/"; \
	echo ""; \
	echo "Done! Next steps:"; \
	echo "  1. cd $$PROJECT_NAME"; \
	echo "  2. Edit research-objective.md — describe your research problem"; \
	echo "  3. Edit research-data.md — describe your datasets"; \
	echo "  4. Run auto-experiment skill to start researching"

# Catch the project name argument so make doesn't complain about missing targets
%:
	@:

list: ## List available skills and rules
	@echo "Skills:"
	@for f in skills/*.md; do echo "  $$(basename $$f .md)"; done
	@echo ""
	@echo "Rules:"
	@for f in rules/*.md; do echo "  $$(basename $$f .md)"; done
