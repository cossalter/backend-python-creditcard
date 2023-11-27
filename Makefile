include ./app/.env
export $(shell sed 's/=.*//' ./app/.env)

setup-local:
	@cd app && rtx exec .rtx.toml -- poetry install
	
run-local:
	@cd app && poetry run uvicorn main:app --host 0.0.0.0 --port 3000 --reload

run-tests:
	@cd app && poetry run pytest -vvv