docker-compose run backend alembic revision --autogenerate -m "initial migration"
docker-compose run backend alembic upgrade head
docker-compose exec db psql -U postgres -d postgres
\dt