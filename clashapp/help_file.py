import pymysql
import config
import pandas as pd
import seaborn as sns

sns.set()

connection = pymysql.connect(host=config._mysql_host,
                             user=config._mysql_user,
                             password=config._mysql_password,
                             db=config._mysql_db,
                             port=config._mysql_port,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

sql = '''
select * from clan_stats_current
'''

with connection.cursor() as cursor:
    # Create a new record
    cursor.execute(sql)
    results = cursor.fetchall()


print(results)

df = pd.DataFrame(results)

print(df)
