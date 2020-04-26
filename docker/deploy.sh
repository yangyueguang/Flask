#!/bin/sh
image_path=yangyueguang/flask:$(date +%Y%m%d%H)
function build_docker() {
#  cp -r ~/.ssh ./
  #--no-cache 确保获取最新的外部依赖 -f 指定文件 ， -t 指定生成镜像名称
  docker build --no-cache -f docker/Dockerfile -t $image_path .
#  rm -rf ./.ssh
}

function push_docker() {
  docker push $image_path
}

function setup() {
  sudo python setup.py build_ext
}

function start() {
  #docker run -itd -p 5001:5001 --name=$image_name --restart=always -v /logs:/logs/logs $image_path:$image_tag
  docker stack deploy --with-registry-auth --prune -c docker-compose.yml monitor
  sleep 5
  docker service ls | grep monitor
}

function stop() {
  docker stack rm monitor
  stopping_container=`docker ps | grep monitor | wc -l`
  while [[ $stopping_container -gt 0 ]]
  do
    echo "${stopping_container} containers are stopping, please wait!"
    sleep 5
    stopping_container=`docker ps | grep monitor | wc -l`
  done
  echo "All stopped"
}