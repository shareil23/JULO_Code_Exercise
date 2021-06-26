# JULO Code Test

JULO Mini Wallet Exercise.

## Stack
|||
|----|-------|
|Language|Python|
|Framework|Flask|
|Database|Postgres|
|Cache|Redis|
|Container|Docker|
|Port Services Running|`8000`|
|Port Database Running|`7000`|


## Current Directory Structure
```bash
├── README.md
├── app.py
├── Documents
├── docker-compose.yml
├── manage.py
├── migration.sh
├── requirements.txt
└── src
    ├── Config
    ├── Controller
    ├── Models
    ├── Schema
    ├── Static
    ├── Templates
    ├── Test
    ├── __init__.py

```

# How To Run The Services

After done clone this repository, make sure docker has installed on the computer, port `8000` and port `7000`
 not used or can change in `docker-compose.yml` file, then execute this command on the shell
`docker-compose up --build` , after that make a new tab in a shell then execute this command to migrate
the database models `docker exec -it julo_mini_wallet_servcies  bash ./migration.sh first`.
Happy testing the services, after done testing the services press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the
services. After that execute the last command `docker-compose down --rmi local -v` to clean up the container.