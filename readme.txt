git checkout sqlalchemy
1. docker-compose up
2. docker-compose exec backend_ehouse_users alembic upgrade head
3. docker-compose exec backend_ehouse_users python manage.py createsuperuser
4. docker-compose exec backend_ehouse_users python manage.py createpermissions

