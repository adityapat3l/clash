with modified_table as (
select
  player_tag, player_name, date(created_time) as created_date, {metric} as metric ,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time) as hour_rank,
  rank() over (PARTITION BY player_tag, date(created_time)order by player_tag, created_time desc) as hour_rank_desc
from player_stats_historic)

select player_tag, player_name,
       '{metric}' as metric,
       created_date as start_date,
       max(case when hour_rank_desc = 1 then metric end) -
          max(case when hour_rank = 1 then metric end) as y0
from modified_table
where player_name = '{player_name}'
GROUP BY 1,2,3, 4
having y0 is not null;