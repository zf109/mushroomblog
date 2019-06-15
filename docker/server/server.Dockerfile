FROM mushroom/base
ADD ./mushroom /mushroom
ADD ./docker/server/entrypoint.sh /entrypoint.sh
ENTRYPOINT chmod +x /entrypoint.sh && /entrypoint.sh
