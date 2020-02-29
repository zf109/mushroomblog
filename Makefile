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

setup:
	docker-compose -f docker/compose/default.yml up -d
	docker run --rm \
	--entrypoint bash \
	-e ALEMBIC_URL=$${ALEMBIC_URL} \
	--volume `pwd`/alembic:/alembic \
	--net compose_default \
	--link mushroom-db \
	mushroom/server -c 'cd alembic && PYTHONPATH=../ alembic upgrade head'
	docker-compose -f docker/compose/default.yml down
