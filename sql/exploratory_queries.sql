-- =====================================================================
-- exploratory_queries.sql
-- Ad-hoc SELECT queries used to explore the data and interpret patterns
-- before/alongside building the Power BI dashboard.
-- =====================================================================

-- Top 10 countries by total watch time
SELECT
    u.country,
    SUM(wh.minutes_watched) AS total_watch_time
FROM watch_history wh
JOIN users u ON wh.user_id = u.user_id
GROUP BY u.country
ORDER BY total_watch_time DESC
LIMIT 10;

-- Average watch time per user by subscription plan
SELECT
    u.subscription_plan,
    SUM(wh.minutes_watched) / COUNT(DISTINCT wh.user_id) AS avg_minutes_per_user
FROM watch_history wh
JOIN users u ON wh.user_id = u.user_id
GROUP BY u.subscription_plan
ORDER BY avg_minutes_per_user DESC;

-- Completion rate by primary genre
SELECT
    t.primary_genre,
    AVG(wh.completed::int) AS completion_rate
FROM watch_history wh
JOIN titles t ON wh.title_id = t.title_id
GROUP BY t.primary_genre
ORDER BY completion_rate DESC;

-- Watch time by hour of day (when are users most active?)
SELECT
    wh.watch_hour,
    SUM(wh.minutes_watched) AS total_watch_time,
    COUNT(*)                AS total_events
FROM watch_history wh
GROUP BY wh.watch_hour
ORDER BY wh.watch_hour;

-- Top 20 titles by total watch time
SELECT
    t.title_name,
    t.primary_genre,
    t.format,
    SUM(wh.minutes_watched) AS total_watch_time,
    AVG(wh.completed::int)  AS completion_rate
FROM watch_history wh
JOIN titles t ON wh.title_id = t.title_id
GROUP BY t.title_name, t.primary_genre, t.format
ORDER BY total_watch_time DESC
LIMIT 20;
