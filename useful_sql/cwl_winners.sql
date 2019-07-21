with subquery as (

 SELECT
   battle_tag,
   season,
  round_number,
  clan_tag,
  clan_stars,
  clan_destruction,
  clan_attacks,
  opponent_clan_tag,
  opponent_stars,
  opponent_destruction,
  opponent_attacks
 FROM
  cwl_rounds

UNION

 SELECT
   battle_tag,
   season,
  round_number,
  opponent_clan_tag,
  opponent_stars,
  opponent_destruction,
  opponent_attacks,
  clan_tag,
  clan_stars,
  clan_destruction,
  clan_attacks
 FROM
  cwl_rounds
)
 select clan_name, sum(clan_stars)
from subquery
LEFT JOIN cwl_clan_current ccc ON (subquery.clan_tag = ccc.clan_tag)
GROUP BY 1;