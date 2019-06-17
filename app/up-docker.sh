#!/bin/bash

db_image_name="scraped-mongo"
db_root="root"

#database
cd ./mongo

if [[ "$(! docker images -q ${db_image_name})" == "" ]]; then
	docker build -t ${db_image_name} .
fi

if [[ "$(! docker ps | grep ${db_image_name})" == "" ]]; then
	sudo docker run -d -p 27017:27017 --name ${db_image_name} -e MONGO_INITDB_ROOT_USERNAME=${db_root} -e MONGO_INITDB_ROOT_PASSWORD=${db_root} ${db_image_name}
else
	echo "Container ${db_image_name} already started"
fi

