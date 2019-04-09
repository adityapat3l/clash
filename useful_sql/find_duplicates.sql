-- FIND DUPLICATE VALUES FOR SAME PLAYER AND SAME HOUR IN PLAYER STATS HISTORIC
SELECT *
FROM player_stats_historic
WHERE (player_tag, created_time) IN (SELECT t2.player_tag, t2.created_time
                                     FROM (SELECT player_tag,
                                                  created_time,
                                                  hour_format,
                                                  (created_time != first_value(created_time) OVER w) AS non_first_ts
                                           FROM (SELECT player_tag,
                                                        created_time,
                                                        date_format(created_time, '%Y-%m-%d %H:00:00') AS hour_format
                                                 FROM player_stats_historic
                                                 GROUP BY 1, 2, 3
                                                 ORDER BY 1, 2, 3) t
                                           WINDOW w AS (PARTITION BY player_tag, hour_format ORDER BY player_tag, created_time))
                                              t2
                                     WHERE non_first_ts = 1);