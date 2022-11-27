# DRF-Plaid

**Tech Stack**
* Python
* Django
* Django REST
* SQLite
* Redis
* Celery

## Routes

```bash
POST register/ => Create a new user, requires {username, password}

POST login/ => Login, returns a login_token on success, requires {username, password}

POST logout/ => Logout, requires {login_token}

POST exchange-token/ => Returns access_token in exchange of public_token, requires {login_token, public_token}

POST get-accounts/ => Returns user accounts, requires {login_token}

POST get-transactions/ => Returns transactions within a given time period, requires {login_token, start_date, end_date}

POST update-transactions-webhook/ => Endpoint that acts as a webhook when new transaction is made using Plaid
```

All the requests are POST requests and the variables in the {} above need to be passed in the body in JSON format.

## Setup

### Python dependancies

```bash
pip install -r requirements.txt 
```
### Install and start Redis Server

I have used Redis server for the celery broker, it uses default URL 'redis://127.0.0.1:6379'.
Also I have used SQLite to store the celery results.

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
celery -A PlaidDjango  --pool=solo worker -l info
```

### Run Django Server
```bash
python manage.py runserver
```

### Ngrok
In order to give a localhost endpoint to Plaid as a public webhook, I have used ngrok.
It can be downloaded from https://ngrok.com/, after installation, ngrok needs to be mapped to the localhost port
where django is running
```bash
ngrok http 8000
```

### Set Plaid Credentials
Setup a Plaid account and add your credentials in ```Task/tasks.py```
```bash
PLAID_CLIENT_ID = "your_client_id"
PLAID_SECRET = "your_secret"
PLAID_ENV = "sandbox"
```

# Best Practices followed

* Item_id, access_token stored in DB, never exposed to the client
* Item model created and associated with webhook so additional API calls are reduced
* Task results stored in DB to view Success/Failure status
* Large tasks moved to celery

# Screenshots

## Signup

### Postman:
![signup_1](https://user-images.githubusercontent.com/72970106/204130698-7728f1ca-bdd7-43de-a794-110c447aee7d.png)

### Result in Admin:
![signup_2](https://user-images.githubusercontent.com/72970106/204130694-ead2d701-d35b-418a-8732-a1474a0df82c.png)

## Login

### Postman:
![login_1](https://user-images.githubusercontent.com/72970106/204130833-23d99825-0cd1-43c7-a77b-59d970dac7b4.png)

### Result in Admin:
![login_2](https://user-images.githubusercontent.com/72970106/204130843-bc2ac130-be84-42f7-8c54-dad9ed87ebe0.png)

## Logout

### Postman:
![logout_1](https://user-images.githubusercontent.com/72970106/204130872-9eb7a35e-5d5d-4743-ab7a-0b4e431a61e4.png)

## Token Exchange

### Create Item:
![exchange_1](https://user-images.githubusercontent.com/72970106/204130898-bae1a455-270d-46bb-ac9b-533232e2fa4a.png)

### Exchange Token:
![exchange_2](https://user-images.githubusercontent.com/72970106/204130901-ca0cfd1f-8fa0-4d4c-a1c2-83037a0a19e9.png)

### Task in Celery:
![exchange_4](https://user-images.githubusercontent.com/72970106/204130904-55db18ab-ab96-4904-9b00-999cb74e84c7.png)

## Transaction update webhook

### Fire webhook in Postman:
![webhook_1](https://user-images.githubusercontent.com/72970106/204130947-d79c6af6-42f5-4ea4-989f-82e0a8269321.png)

### Task in Celery:
![webhook_3](https://user-images.githubusercontent.com/72970106/204130951-77276759-3c9d-4274-a8fc-a4cce22a171f.png)

### Status in ngrok:
![webhook_4](https://user-images.githubusercontent.com/72970106/204130954-355420e7-91ea-4401-a11a-3dab157f32bd.png)

## Fetch Account Data

### Postman:
![accounts_1](https://user-images.githubusercontent.com/72970106/204131026-80c0f7b5-b447-4055-8991-bee171d94e90.png)

### Task in Celery:
![accounts_2](https://user-images.githubusercontent.com/72970106/204131030-0deaf96c-1e8b-4c08-b7c7-de9c4ced0a30.png)

## Fetch All Transactions

### Postman:
![transactions_1](https://user-images.githubusercontent.com/72970106/204131084-1ee20a0f-4545-484b-bb16-38d9659273d4.png)

### Task in Celery:
![transactions_2](https://user-images.githubusercontent.com/72970106/204131088-ade0d09e-ce38-43a5-b886-87baa2855dd7.png)

## Task Results

![task_status](https://user-images.githubusercontent.com/72970106/204131165-fcf58869-7feb-45a1-aef3-dfb4d6372033.png)










































