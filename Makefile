.PHONY: format
format:
	black meggie_sourceanalysis

.PHONY: check
check:
	black --check meggie_sourceanalysis
	pylama meggie_sourceanalysis

.PHONY: test
test:
	pytest -s
