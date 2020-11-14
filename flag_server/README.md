# Client launch

Just run it:
``` sh
python3 client.py -ht [ip_addr] -p [port]
```

# Server launch

1. Install & configure postgresql database:
``` sh
sudo apt install postgresql
sudo su - postgres
createuser --interactive --pwprompt  
    telepathy  
    <password>  
    no  
    yes  
    no  
createdb telepathy
psql
GRANT ALL PRIVILEGES ON DATABASE "telepathy" to telepathy;

# log off from postgres

# Change database port to 5431
# path and version number depends on distribution
sudo vim /etc/postgresql/11/main/postgresql.conf
```

2. Install python dependencies and local libraries if needed:
``` sh
pip install -r requirements_server.txt

# If error from psycopg2
sudo apt install python3-psycopg2
sudo apt install libpq-dev
pip install -r requirements_server.txt

```

3. Create *.env* file or create variable *FLAG_DB_PASSWORD* with chosen password (or change hardcoded variable from server.py 19 line)
4. Create *flags.json* file with format:
``` json
[
    {
        "taskname": "string taskname",
        "lab_no": int,
        "flag": "string flag",
        "points": int
    }
]
```
5. Run *server.py* for first time with *-idb* flag (other are optional):
``` sh
# This will init database and upload tasks from file
python3 server.py -idb
```