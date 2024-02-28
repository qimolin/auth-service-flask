# Auth Service Flask
This repo is part of the UvA course Web Services and Cloud-Based Systems. It is a simple auth service implemented in Flask.

## Dependencies
- Python 3.11
- Flask
- PyMongo
- Docker

## Create a venv
```bash
python -m venv .venv
. .venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```
## Create a .env file
```bash
set PRIVATE_KEY_PASSWORD to a password
```

## Run the app (with reload)
```bash
python app.py --reload
```

## Run the app with Docker
```bash
docker build -t auth-service-flask .
docker run -p 5001:5001 auth-service-flask
```

## Install mongodb [(Install guide)](https://www.mongodb.com/docs/manual/administration/install-community/)
### Linux
```bash
sudo apt-get install gnupg curl

curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \

sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org
```

### MacOS
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

## To test data persistence
1- run `docker-compose up -d`
2- run tests to populate data `python3 test_auth.py`
3- test data persists after running `docker-compose restart`
   - `docker exec -it auth-service-flask-mongo-1 bash`
   - `mongosh`
   - use admin `db.getSiblingDB('admin').auth('root', 'example');` 
   - user data persists `db.users.find({})`
5 - `docker-compose down`
6 - `docker-compose up -d`
7 - Repeat step 3 to ensure user data still persists


