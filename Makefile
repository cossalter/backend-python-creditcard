run-local:
	@cd app && poetry run uvicorn main:app --host 0.0.0.0 --port 3000 --reload

setup-local:
	@cd app && rtx exec .rtx.toml -- poetry install