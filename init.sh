#! /bin/bash
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

sudo ln -sf /home/box/web/etc/gunicorn-django.conf /etc/gunicorn.d/test-django
sudo ln -sf /home/box/web/etc/gunicorn-wsgi.conf /etc/gunicorn.d/test-wsgi
sudo /etc/init.d/gunicorn restart
 
#sudo gunicorn -b 0.0.0.0:8080 hello:ws &
#sudo gunicorn -b 0.0.0.0:8000 ask.wsgi:application & 
