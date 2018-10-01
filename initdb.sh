sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE ask;"
python3 manage.py makemigrations qa
python3 manage.py maigrate
#mysql -uroot -e "CREATE USER 'user'@'localhost' IDENTIFIED BY '123';"
#mysql -uroot -e "GRANT ALL ON *.* TO 'user'@'localhost';"
#mysql -uroot -e "FLUSH PRIVILEGES;"
