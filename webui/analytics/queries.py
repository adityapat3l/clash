from clashapp import db
from sqlalchemy.sql import text
import datetime


SQL_QUERY = """ select count(*) from player_stats_current where created_time >= :created_time"""

with db.engine.connect() as con:

    query = text(SQL_QUERY)
    cur = con.execute(query, created_time=datetime.datetime(2019, 4, 10))

    results = cur.fetchall()
    headers = cur.keys()

print(results)

