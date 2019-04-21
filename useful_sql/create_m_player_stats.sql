create TABLE m_player_stats (
  player_tag VARCHAR(20),
  player_name VARCHAR(80),
  metric varchar(256),
  start_date datetime,
  y0 int(8),
  PRIMARY KEY (player_tag, metric, start_date)
)
;
