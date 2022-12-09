# BACK-PFE

Create env file

```
DB_HOST=<DB_HOST>
DB_USER=<DB_USER>
DB_PASS=<DB_PASSWORD>
DB_NAME=<DB_NAME>
DB_PORT=5432
LOG_NAME=<LoggerName>
JWT_SECRET=<JWT_SECRET>
PATH_LOGS=<DIR_LOG/LOG.TXT>
PORT=<SERVER_PORT>

STORAGE_ACCOUNT_KEY=<STORAGE_ACCOUNT_KEY>
STORAGE_ACCOUNT_NAME=<STORAGE_ACCOUNT_NAME>
CONNECTION_STRING=<CONNECTION_STRING>
CONTAINER_NAME=<CONTAINER_NAME>
```

Install the requirements
```python
pip3 install -r "requirements.txt"
```
Launch the server with app.py
```python
python app.py
```