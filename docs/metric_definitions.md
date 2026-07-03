# Metric Definitions & Assumptions

This document defines the core metrics, data model terms, and reporting assumptions used in the Power BI dashboard to ensure consistency across pages and visuals.

## Core Metrics

### Total Watch Time
**Definition:** Total number of minutes watched across all viewing events in the selected filter context.  
**DAX logic:** `SUM(watch_history[minutes_watched])`

### Active Users
**Definition:** Number of unique users with at least one watch event in the selected filter context.  
**DAX logic:** `DISTINCTCOUNT(watch_history[user_id])`

### Total Events
**Definition:** Total number of watch events (viewing sessions) recorded in the selected filter context.  
**DAX logic:** `COUNTROWS(watch_history)`

### Avg Watch Time per User
**Definition:** Average total minutes watched per active user.  
**DAX logic:** `DIVIDE([Total Watch Time], [Active Users])`

### Avg Minutes per Event
**Definition:** Average number of minutes watched per viewing event.  
**DAX logic:** `DIVIDE([Total Watch Time], [Total Events])`

### Completed Views
**Definition:** Number of viewing events classified as completed.  
**DAX logic:** Sum or count of rows where `completed = TRUE` (or `1`, depending on the final data type used in Power BI).

### Completion Rate
**Definition:** Share of watch events that were completed.  
**DAX logic:** `DIVIDE([Completed Views], [Total Events])`

---

## Data Model Definitions

### Fact Table: `watch_history`
Contains event-level streaming activity, including:
- user
- title
- watch date
- watch hour
- device type
- minutes watched
- completion flag

### Dimension Table: `users`
Contains user-level attributes, including:
- country
- subscription plan
- signup date

### Dimension Table: `titles`
Contains content-level attributes, including:
- title name
- genre
- release year
- content rating
- format (Movie/Series)
- original content flag
- duration

---

## Reporting Assumptions

### Synthetic data assumption
All data in this project is synthetic and was generated for portfolio/demo purposes. The dataset is designed to resemble realistic streaming-platform behavior but does not represent real customer data.

### Completion assumption
A viewing event is considered **completed** when `minutes_watched` is greater than or equal to approximately **70% of the title duration**.

### Engagement assumption
Higher watch time, higher completion rate, and higher average minutes per event are treated as signals of stronger user engagement.

### Filter context assumption
All KPI values shown in Power BI are dynamic and update based on the current page filters and slicers, such as country, subscription plan, date range, and content type.

### Granularity assumption
`watch_history` is modeled at the **event level**, meaning each row represents one viewing session for one user and one title at a specific point in time.

### Time-of-day assumption
`watch_hour` is stored as an integer from `0` to `23`, representing the hour of the day in which the viewing event occurred.

---

## Why This Documentation Matters

Documenting metric definitions and assumptions helps ensure:

- KPI calculations are interpreted consistently across dashboard pages
- business terms such as “active users” and “completion rate” are clearly defined
- future dashboard updates use the same metric logic
- reporting remains transparent and reproducible
