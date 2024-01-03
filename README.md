# Running Project

MySQL database is running on Docker Container via Compose.
Flask App is running from local.

## Running MySQL Container

To Run MySQL Container, run this command on project directory.

```shell
docker-compose up
```

If you add new table to init.sql, first run

```shell
docker-compose down -v
```

and then

```shell
docker-compose up --build
```

## To Run Flask App

First install requirements by

```shell
pip install -r requirements.txt
```

And run this command to run flask app

```shell
flask run
```
You may not run flask on 5000 port if you are Mac user.
You can run on custom port such as 8000:

```shell
flask run -p 8000
``````

## Authors

[Kaan Karataş - 150200081](https://github.com/necrocultist)

[Helin Aslı Aksoy - 150200705](https://github.com/helinasli)

[Ayça Tulum - 150200057](https://github.com/atulum)

[Eren Culhacı - 150220763](https://github.com/erenculhaci)
