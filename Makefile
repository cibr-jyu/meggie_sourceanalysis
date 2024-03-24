.PHONY: format
format:
	black -t py39 meggie_sourceanalysis

.PHONY: check
check:
	black --check -t py39 meggie_sourceanalysis
	pylama meggie_sourceanalysis

.PHONY: test
test:
	pytest -s
