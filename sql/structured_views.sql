-- =====================================================================
-- structured_views.sql
-- Reusable analytical views that turn raw event-level data into
-- structured, analysis-ready datasets for trend and performance work.
-- These views are the SQL layer feeding downstream BI and Excel analysis.
-- =====================================================================

-- Daily engagement trend (one row per calendar day)
CREATE VIEW vw_daily_engagement AS
SELECT
    wh.watch_date,
    COUNT(DISTINCT wh.user_id)                AS active_users,
    COUNT(*)                                  AS total_events,
    SUM(wh.minutes_watched)                   AS total_watch_time,
    AVG(wh.minutes_watched)                   AS avg_minutes_per_event,
    AVG(wh.completed::int)                    AS completion_rate
FROM watch_history wh
GROUP BY wh.watch_date;

-- Engagement by subscription plan
CREATE VIEW vw_plan_engagement AS
SELECT
    u.subscription_plan,
    COUNT(DISTINCT wh.user_id)                AS active_users,
    SUM(wh.minutes_watched)                   AS total_watch_time,
    SUM(wh.minutes_watched)
        / COUNT(DISTINCT wh.user_id)          AS avg_minutes_per_user,
    AVG(wh.completed::int)                    AS completion_rate
FROM watch_history wh
JOIN users u ON wh.user_id = u.user_id
GROUP BY u.subscription_plan;

-- Engagement by country
CREATE VIEW vw_country_engagement AS
SELECT
    u.country,
    COUNT(DISTINCT wh.user_id)                AS active_users,
    SUM(wh.minutes_watched)                   AS total_watch_time,
    COUNT(*)                                  AS total_events
FROM watch_history wh
JOIN users u ON wh.user_id = u.user_id
GROUP BY u.country;

-- Content performance by genre (joins the titles dimension)
CREATE VIEW vw_genre_performance AS
SELECT
    t.primary_genre,
    COUNT(DISTINCT wh.title_id)               AS titles_watched,
    SUM(wh.minutes_watched)                   AS total_watch_time,
    AVG(wh.minutes_watched)                   AS avg_minutes_per_event,
    AVG(wh.completed::int)                    AS completion_rate
FROM watch_history wh
JOIN titles t ON wh.title_id = t.title_id
GROUP BY t.primary_genre;

-- Device usage summary
CREATE VIEW vw_device_engagement AS
SELECT
    wh.device_type,
    COUNT(*)                                  AS total_events,
    SUM(wh.minutes_watched)                   AS total_watch_time,
    AVG(wh.completed::int)                    AS completion_rate
FROM watch_history wh
GROUP BY wh.device_type;
