#!/bin/bash

db_image_name="scraped-mysql"
db_root_password="root"

#database
cd ./mysql

if [[ "$(! docker images -q ${db_image_name})" == "" ]]; then
	docker build -t ${db_image_name} .
fi

if [[ "$(! docker ps | grep ${db_image_name})" == "" ]]; then
	sudo docker run -d -p 3306:3306 --name ${db_image_name} -e MYSQL_ROOT_PASSWORD=${db_root_password} ${db_image_name}
else
	echo "Container ${db_image_name} already started"
fi

