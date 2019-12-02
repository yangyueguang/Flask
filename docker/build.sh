#!/bin/sh
cd ..
TIMENOW=`date +%Y%m%d%H`
image_tag=${TIMENOW}
image_name=logs_upload
image_path=dockerhub.datagrand.com/zz57/$image_name
# 把本地密钥拷到镜像
cp -r ~/.ssh ./
#--no-cache 确保获取最新的外部依赖 -f 指定文件 ， -t 指定生成镜像名称 ， 冒号后为版本号 ， 各位大佬命名请不要冲突 例子 ： rec_action_pipe:17.08.01.1311
docker build --no-cache -f docker/Dockerfile -t $image_path:$image_tag .
rm -rf ./.ssh
#docker tag $image_path:$image_tag $image_path:latest
docker images | grep $image_name
#docker save $image_path:$image_tag -o deploy/$image_name.$image_tag.tar &
echo $image_path:$image_tag

