select
    m.player_name,
   clan_name,
    town_hall_level,
    sum(case when start_date = '2019-05-02' then metric_value end) as war_1_stars,
    sum(case when start_date = '2019-05-03' then metric_value end) as war_2_stars,
    sum(case when start_date = '2019-05-04' then metric_value end) as war_3_stars,
    sum(case when start_date = '2019-05-05' then metric_value end) as war_4_stars,
    sum(metric_value) as total_stars_earned
from m_player_stats m
left join player_stats_current psc ON (psc.player_tag = m.player_tag COLLATE utf8_unicode_ci)
left join clan_stats_current csc on psc.clan_tag  = csc.clan_tag
where csc.clan_tag in ('#YUPCJJCR','#9L8QLQ9U', '#28GP9VJLL', '#GP0UP0CG', '#9JG02C0Q', '#8UGQ208P', '#9YRCG02Y', '#9LR0V8LG')
and metric_name = 'war_stars'
and start_date >= '2019-05-02'
GROUP BY 1,2,3
order by total_stars_earned desc
;