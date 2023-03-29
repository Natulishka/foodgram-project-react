# Foodgram

![example workflow](https://github.com/Natulishka/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Описание


### Стек технологий:  

Python 3.7  
Django 2.2.16  
DRF 

Развернуть докер контэйнеры::
```
docker-compose up -d
```
Выполнить миграции, создать суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Загрузить начальные данные (ингрединеты, теги, авторов):
```
docker-compose exec web python manage.py load_data
```

Удаить все контейнеры с volume
```
docker-compose down -v
```
Удалить все образы
```
docker system prune -a
```
Удалить образ web
```
docker rmi infra-web
```
Полностью перезапустить web
```
docker stop infra-web-1 && docker rm infra-web-1 && docker rmi infra-web && docker-compose up -d
```


Как скопировать файл по SSH с локальной машины на удалённый сервер
Как загрузить файл на сервер по SSH? Для этого используйте команду вида:
```
scp [путь к файлу] [имя пользователя]@[имя сервера/ip-адрес]:[путь к файлу]
```
Пример команды:
```
scp /home/test.txt root@123.123.123.123:/directory
```
Файл test.txt будет скопирован на хост 123.123.123.123 в директорию «/directory».


Обновление системы
обновите индекс пакетов APT:
```
sudo apt update
```
Теперь обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```