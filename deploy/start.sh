#!/bin/sh
#docker run -itd -p 5001:5001 --name=$image_name --restart=always -v /logs:/logs/logs $image_path:$image_tag
docker stack deploy --with-registry-auth --prune -c docker-compose.yml monitor
sleep 5
docker service ls | grep monitor