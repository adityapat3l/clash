from clashapp import db
from sqlalchemy.sql import text
import datetime
from contextlib import closing
from datetime import timedelta

# I would create a real TEMP table but my Mysql host does't let me
CREATE_TEMP_TABLE = """ 
create table temp_modified_table as (
select
  player_tag, player_name, date(created_time) as created_date, {metric} as metric_value ,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time) as hour_rank,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time desc) as hour_rank_desc
from player_stats_historic);"""

CREATE_STAGING_TABLE = """
create table temp_m_player_stats (
  player_tag VARCHAR(20),
  player_name VARCHAR(80),
  metric_name varchar(80),
  start_date date,
  metric_value int(8),
  PRIMARY KEY (player_tag, metric_name, start_date)
) CHARSET=utf8;"""

INSERT_INTO_STAGING = """
insert into temp_m_player_stats (player_tag, player_name, metric_name, start_date, metric_value)
select player_tag, player_name,
       '{metric}' as metric_name,
       created_date as start_date,
       max(case when hour_rank_desc = 1 then metric_value end) -
          max(case when hour_rank = 1 then metric_value end) as metric_value
from temp_modified_table
where 
created_date between :start_date and current_date - interval 1 day
GROUP BY 1,2,3, 4
having metric_value is not null"""

DELETE_DUPLICATE_DATA = """
delete from ps
using m_player_stats ps
inner join temp_m_player_stats tmps ON (tmps.player_tag = ps.player_tag AND
                                 tmps.metric_name = ps.metric_name AND
                                 tmps.start_date = ps.start_date);"""

INSERT_DATA = """ INSERT INTO m_player_stats (
                  SELECT * FROM temp_m_player_stats)"""

DROP_STAGING_TABLE =  """ DROP TABLE temp_m_player_stats;"""
DROP_TEMP_TABLE = """ DROP TABLE temp_modified_table;"""

COLUMN_METRICS = ['achv_dark_looted', 'achv_gold_looted', 'achv_elixer_looted', 'achv_total_donations',
                  'achv_th_destroyed', 'battle_machine_level','warden_level', 'queen_level', 'king_level',
                  'town_hall_level', 'war_stars', 'donations_received', 'donations_given',
                  'attack_wins', 'defense_wins', 'current_trophies', 'exp_level']


def populate_m_player_stats(metric_name, start_date=datetime.datetime(2019, 4, 8)):
    with closing(db.engine.connect()) as con:

        create_table_stmt = text(CREATE_TEMP_TABLE.format(metric=metric_name))
        create_staging_table = text(CREATE_STAGING_TABLE)
        insert_staging_table = (text(INSERT_INTO_STAGING.format(metric=metric_name)))
        delete_dups = text(DELETE_DUPLICATE_DATA)
        insert_new_data = text(INSERT_DATA)
        drop_staging = text(DROP_STAGING_TABLE)
        drop_statement = text(DROP_TEMP_TABLE)

        con.execute(create_table_stmt)
        con.execute(create_staging_table)
        con.execute(insert_staging_table, start_date=start_date)
        con.execute(delete_dups)
        con.execute(insert_new_data)
        con.execute(drop_statement)
        con.execute(drop_staging)


def run_populate(start_date):
    for col_name in COLUMN_METRICS:
        populate_m_player_stats(col_name, start_date=start_date)


if __name__ == '__main__':
    query_start_date = datetime.datetime.utcnow() - timedelta(days=1)
    run_populate(run_populate(query_start_date.date()))
