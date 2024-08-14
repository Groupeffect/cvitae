lint:
	pwd && ls
	docker run \
		-e LOG_LEVEL=ERROR \
		-e RUN_LOCAL=true \
		-e VALIDATE_ALL_CODEBASE=true \
		-e SAVE_SUPER_LINTER_SUMMARY=true \
		-e SUPER_LINTER_SUMMARY_FILE_NAME=linter_report.md \
		-e SAVE_SUPER_LINTER_OUTPUT=true \
		-e IGNORE_GITIGNORED_FILES=true \
		-v ./:/tmp/lint \
		--rm \
		github/super-linter:latest > linter_report.md
# ghcr.io/super-linter/super-linter:latest