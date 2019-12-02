#!/bin/sh
cd ..
TIMENOW=`date +%Y%m%d%H`
image_tag=${TIMENOW}
image_name=logs_upload
image_path=dockerhub.datagrand.com/zz57/$image_name
docker login dockerhub.datagrand.com -u xuechao -p Super@123456
docker push $image_path:$image_tag
file=deploy/docker-compose.yml
cat $file | grep dockerhub.datagrand.com | grep $image_name | awk -F ':' '{print $3}' | while read line
do
    sed -i "" "s/${line}/$image_tag/" $file
done
sed -i '' 's/${image_name}:.*$/${image_name}:.${image_tag}/' $file
echo $image_path:$image_tag