init:
	code .
	poetry config --local virtualenvs.create true
	poetry config --local virtualenvs.in-project true
	poetry env use 3.10
	# poetry env use 3.11
	poetry install
	poetry update
	git init
	echo ".venv/" >> .gitignore
	echo "logs/" >> .gitignore
	git lfs install
	git lfs track "*.fit"
	git lfs track "*.hdf5"
	# git lfs track "*.html"
	git lfs track "*.parquet"
	git add .
	poetry run pre-commit run --all-files
	git commit -am "Initial commit after initializing the project."
	poetry shell

test:
	pytest .

coverage:
	pytest --cov=camminapy tests/

cov:
	make coverage

doc:
	pdoc camminapy -o docs  --docformat numpy

publish:
	poetry run pyclean .
	poetry run pre-commit run --all-files
	make test
	poetry export -f requirements.txt --output requirements.txt
	poetry version patch
	poetry publish --build
	git commit -am "Version bump."
	git push


full:
	poetry version patch
	poetry publish --build
	make doc
	pre-commit run --all || true
	pre-commit run --all
	git commit -am "Update doc."
	git push
