-- Existen patrones estadísticos para los días de la semana?
CREATE OR REPLACE VIEW weekday_table AS
WITH weekday_returns AS (
    SELECT
        day_name,
        LOG(dollar_exchange_rate)-LOG(LAG(dollar_exchange_rate) OVER (ORDER BY date)) AS log_returns
    FROM exchange_rates
)
SELECT
    day_Name,
    COUNT(log_returns)    AS n_days,
    AVG(log_returns)     AS avg_return,
    STDDEV(log_returns)      AS volatility,
    SUM(CASE WHEN log_returns > 0 THEN 1 ELSE 0 END)::float / COUNT(*)       AS pct_positive_days,
    (AVG(log_returns)/(STDDEV(log_returns)/SQRT(COUNT(*))))       AS t_stat
FROM weekday_returns
GROUP BY day_name
ORDER BY
  CASE day_name
    WHEN 'Monday' THEN 1
    WHEN 'Tuesday' THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4
    WHEN 'Friday' THEN 5
    WHEN 'Saturday' THEN 6
    WHEN 'Sunday' THEN 7
  END;

SELECT * FROM exchange_rates;
SELECT * FROM weekday_table;