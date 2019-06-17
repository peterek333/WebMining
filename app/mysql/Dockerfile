FROM mysql

ENV MYSQL_DATABASE=scraped
ENV MYSQL_USER=scraper
ENV MYSQL_PASSWORD=scraper

COPY ./scripts/ /docker-entrypoint-initdb.d/
