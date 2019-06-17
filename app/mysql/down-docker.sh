#!/bin/bash

db_image_name="scraped-mysql"

sudo docker stop ${db_image_name}
sudo docker rm ${db_image_name}
