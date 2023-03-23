# praktikum_new_diplom

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
