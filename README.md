## PostgreSQL setup for local DEV

```
sudo su - postgres

psql -p <port>

CREATE DATABASE mail_khaifa;
CREATE USER mail_khaifa_user WITH PASSWORD 'mail_khaifa_user_pwd';
ALTER ROLE mail_khaifa_user SET client_encoding TO 'utf8';
ALTER ROLE mail_khaifa_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mail_khaifa_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mail_khaifa TO mail_khaifa_user;

ALTER ROLE  mail_khaifa_user CREATEDB ; #Required only for running Unit tests locally.
\q

```

The DB connection string is  `postgres://mail_khaifa_user:mail_khaifa_user_pwd@localhost:5433/mail_khaifa`

Udpdate your .env file's `DATABASE_URL`

Connect to DB from command line using psql - 
```
psql -d postgres://mail_khaifa_user:mail_khaifa_user_pwd@localhost:5433/mail_khaifa
```

## Running Tests

```
./run_tests.sh
```