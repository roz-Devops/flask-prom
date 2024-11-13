# Use MySQL 5.7 as base image
FROM mysql:8.3

# Environment variables
ENV MYSQL_DATABASE demo_db
ENV MYSQL_USER user
ENV MYSQL_PASSWORD password
ENV MYSQL_ROOT_PASSWORD password

# Expose port 3306
EXPOSE 3306

# Copy SQL scripts to initialize database
COPY ./dump /docker-entrypoint-initdb.d
