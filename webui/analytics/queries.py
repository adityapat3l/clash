from clashapp import db
from sqlalchemy.sql import text


# I would create a real TEMP table but my Mysql host does't let me
SQL_QUERY = """ 
        select count(*) from player_stats_current
"""

with db.engine.connect() as con:

    query = text(SQL_QUERY)
    cur = con.execute(query)

    results = cur.fetchall()
    headers = cur.keys()


