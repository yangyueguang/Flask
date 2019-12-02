docker stack rm monitor
stopping_container=`docker ps | grep monitor | wc -l`
while [[ $stopping_container -gt 0 ]]
do
    echo "${stopping_container} containers are stopping, please wait!"
    sleep 5
    stopping_container=`docker ps | grep monitor | wc -l`
done
echo "All stopped"