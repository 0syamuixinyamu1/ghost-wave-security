.PHONY: install test lint benchmark clean

install:
	python -m pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check .

benchmark:
	python experiments/run_benchmark.py --config experiments/configs/default.toml

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist src/*.egg-info
