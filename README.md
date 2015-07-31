# dcms
a django based cms

## init db
sudo -i -u postgres
psql
CREATE USER dcms PASSWORD 'dcms'; | DROP USER dcms; 
CREATE DATABASE dcms_dev; | DROP DATABASE dcms_dev;
GRANT ALL PRIVILEGES ON DATABASE dcms_dev to dcms; | REVOKE ALL ON DATABASE dcms_dev FROM dcms;
