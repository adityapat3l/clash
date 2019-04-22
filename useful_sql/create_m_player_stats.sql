create TABLE m_player_stats (
  player_tag VARCHAR(20),
  player_name VARCHAR(80),
  metric_name varchar(80),
  start_date date,
  metric_value int(8),
  PRIMARY KEY (player_tag, metric_name, start_date)
) CHARSET=utf8;