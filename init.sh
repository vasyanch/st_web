#! /bin/bash
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

#sudo ln -sf /home/box/web/etc/gunicorn.config /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn start
 
sudo gunicorn -b 0.0.0.0:8080 hello:ws &
sudo gunicorn -c 0.0.0.0:8000 ask.wsgi:application & 
