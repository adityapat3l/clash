from clashapp import db
from sqlalchemy.sql import text


# I would create a real TEMP table but my Mysql host does't let me
CREATE_TEMP_TABLE = """ 
create table temp_modified_table as (
select
  player_tag, player_name, date(created_time) as created_date, {metric} as metric_value ,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time) as hour_rank,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time desc) as hour_rank_desc
from player_stats_historic);
"""

INSERT_INTO_TABLE = """
insert into m_player_stats (player_tag, player_name, metric_name, start_date, metric_value)

select player_tag, player_name,
       '{metric}' as metric_name,
       created_date as start_date,
       max(case when hour_rank_desc = 1 then metric_value end) -
          max(case when hour_rank = 1 then metric_value end) as metric_value
from temp_modified_table
where player_name = '{player_name}'
GROUP BY 1,2,3, 4
having metric_value is not null;"""

DROP_TEMP_TABLE = """ DROP TABLE temp_modified_table"""

COLUMN_METRICS = ['achv_dark_looted', 'achv_gold_looted', 'achv_elixer_looted', 'achv_total_donations',
                  'achv_th_destroyed', 'battle_machine_level','warden_level', 'queen_level', 'king_level',
                  'town_hall_level', 'war_stars', 'donations_received', 'donations_given',
                  'attack_wins', 'defense_wins', 'current_trophies', 'exp_level']

metric_name = 'achv_dark_looted'
with db.engine.connect() as con:

    create_table_stmt = text(CREATE_TEMP_TABLE.format(metric=metric_name))
    insert_statement = text(INSERT_INTO_TABLE.format(metric=metric_name, player_name='adi'))
    drop_statement = text(DROP_TEMP_TABLE)

    con.execute(create_table_stmt)
    con.execute(insert_statement)
    con.execute(drop_statement)


