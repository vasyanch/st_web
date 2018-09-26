mysql -uroot -e CREATE USER vasya@localhost;
mysql -uroot -e CREATE DATABASE ask;
mysql -uroot -e GRANT ALL ON mysite.* TO vasya@localhost;
