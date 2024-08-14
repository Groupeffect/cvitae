lint:
	pwd && ls
	docker run \
		-e LOG_LEVEL=ERROR \
		-e RUN_LOCAL=true \
		-e VALIDATE_ALL_CODEBASE=true \
		-e SAVE_SUPER_LINTER_SUMMARY=true \
		-e SUPER_LINTER_SUMMARY_FILE_NAME=linter_report.md \
		-e SAVE_SUPER_LINTER_OUTPUT=true \
		-e SUPER_LINTER_OUTPUT_DIRECTORY_NAME=/tmp/lint \
		-e IGNORE_GITIGNORED_FILES=true \
		-e FIX_ENV=true \
		-e FIX_PYTHON_BLACK=true \
		-e VALIDATE_HTML=false \
		-e PYTHONDONTWRITEBYTECODE=1 \
		-v ./:/tmp/lint \
		--rm \
		github/super-linter:latest

cleanup:
	black .

setupenv:
	python -m venv cvenv
	source cvenv/bin/activate
	pip install black
	pip --no-cache-dir -r install app/requirements.txt

dcu:
	docker-compose up
dcd:
	docker-compose down
dcb:
	docker-compose up --build --remove-orphans
