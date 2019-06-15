docker build $1 -t mushroom/base -f docker/base.Dockerfile .
docker build $1 -t mushroom/server -f docker/server/server.Dockerfile .
