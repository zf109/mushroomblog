.PHONY: tests

run:
	sh ./docker/build.sh
	sh ./localstack.sh up

tests:
	PYTHONPATH=. pytest $$(find . | grep tests.py)

db_kaboom:
	# clear everything in db
	cd alembic && PYTHONPATH=../ alembic downgrade base

db_create:
	# upgrade to head
	cd alembic && PYTHONPATH=../ alembic upgrade head
