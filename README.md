# Django-Plaid

```bash
POST /register/ => Create a new user, requires {email, password}

POST /login/ => Login, returns a token on success, requires {email, password}

POST /logout/ => Logout, requires {token}

GET /token-exchange/ => Returns access_token in exchange of public token, requires {email, public_token}

GET /get-transactions/ => Returns transactions within a given time period, requires {email, start_date, end_date}

GET /get-accounts/ => Returns user account, requires {email}

POST /update-transaction/ => Exposed webhook for fetching transactions, requires {email, transaction_id}
```

## Setup

### Python dependancies

```bash
pip install -r requirements.txt 
```
### Install and start Redis Server

I have used Redis server for the celery broker, it uses default URL 'redis://127.0.0.1:6379'

```bash
Celery Broker -> Redis
Celery Backend -> SQLite
```


### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Celert Worker
```bash
celery -A PlaidDjango  worker -l info
```

### Run Django Server
```bash
python manage.py runserver
```



