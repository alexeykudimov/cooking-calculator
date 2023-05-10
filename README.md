## :zap: Cooking calculator service

### :dart: Technologies
* Python 3.11
* FastAPI
* PostgreSQL
* Async SQLAlchemy 2.0
* Async Alembic
* Async Pytest
### :dart: Environment
    SECRET_KEY=<your secret key>

    DATABASE_URL=postgresql+asyncpg://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    TEST_DATABASE_URL=postgresql+asyncpg://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
### :dart: Build
    docker-compose up -d
### :dart: Migrate
    docker exec -it server alembic upgrade heads
### :dart: Tests
    docker exec -it server pytest -v -s tests
### :dart: Let's go!
    http://localhost:8000/docs/