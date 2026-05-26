SELECT *
FROM {{ ref('mart_apps_summary') }}
ORDER BY installs DESC
LIMIT 20