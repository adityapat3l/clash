


SQL_QUERY = """
select 
    concat(datediff(current_date, start_date), ' Day(s) Ago') as days_ago,
    metric_value
from m_player_stats
where 
metric_name = '{metric_name}'
{sql_text}
order by start_date desc
limit {max_len}"""
