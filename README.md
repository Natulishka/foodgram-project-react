# Foodgram

![example workflow](https://github.com/Natulishka/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание

Сайт Foodgram ("Продуктовый помощник"). Это онлайн-сервис и API для него. С его помощью пользователи могут публиковать рецепты, подписываться на других пользователей, добавлять понравившиеся рецепты в список Избранное или в Список покупок, а также скачивать сводный список ингредиентов, необходимых для приготовления одного или нескольких выбранных блюд в формате txt или pdf.

## Стек технологий:

```
Python 3.7  
Django 3.2.18  
DRF
Gunicorn
Nginx
```

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Natulishka/foodgram-project-react.git
cd infra/
```

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

## Полезные команды

Удалить все контейнеры вместе с volume
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
Скопировать файл по SSH с локальной машины на удалённый сервер
```
scp [путь к файлу] [имя пользователя]@[имя сервера/ip-адрес]:[путь к файлу]
```
Пример команды:
```
scp /home/test.txt root@123.123.123.123:/directory
```
Файл test.txt будет скопирован на хост 123.123.123.123 в директорию «/directory».  


## Документация  


Документацию и примеры запросов можно посмотреть по адресу после запуска проекта http://127.0.0.1/api/docs/

## Развернутый проект

http://51.250.100.218/ - регистрация  
http://51.250.100.218/api/docs/ - документация  
http://51.250.100.218/admin/ - админ панель

## Авторизация в админ панели

email    - admin@ya.ru  
password - admin
