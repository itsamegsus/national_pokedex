import psycopg2
from psycopg2 import sql
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from config import config

DBNAME = "postgres"
DBUSER = "postgres"
DBPASS = "admin"
DBHOST = "localhost"

try:
    con = psycopg2.connect(
        dbname = DBNAME,
        user = DBUSER, 
        host = DBHOST,
        password = DBPASS
    )
    # con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    con.autocommit = True
    cur = con.cursor()
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier("pokedex")))
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("pokedex")))
    cur.close()
    con.commit()
    
except Exception as e:
    print(e)
finally: 
    if con is not None:
        con.close()
