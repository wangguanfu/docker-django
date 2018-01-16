# django-docker

docker build -t mysite/mmcsite .
docker run -d -p 80:80 -v $(pwd):/code --env DJANGO_PRODUCTION=false mysite/mmcsite