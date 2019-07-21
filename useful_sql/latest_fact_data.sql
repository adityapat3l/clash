with subquery as (select *, row_number() over (PARTITION BY player_tag ORDER BY fact_time desc) as entry
from fact_troop)
select *
from subquery
where entry = 1
;
