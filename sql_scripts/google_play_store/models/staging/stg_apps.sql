WITH source AS (

    SELECT *
    FROM {{ source('raw', 'raw_apps') }}

),

cleaned AS (

    SELECT

        TRIM(app) AS app,

        TRIM(category) AS category,

        SAFE_CAST(rating AS FLOAT64) AS rating,

        SAFE_CAST(reviews AS INT64) AS reviews,

        SAFE_CAST(
            REGEXP_REPLACE(installs, '[+,]', '')
            AS INT64
        ) AS installs,

        CASE
            WHEN size = 'Varies with device' THEN NULL
            ELSE TRIM(size)
        END AS size,

        INITCAP(type) AS app_type,

        SAFE_CAST(
            REGEXP_REPLACE(price, '[$]', '')
            AS FLOAT64
        ) AS price,

        TRIM(content_rating) AS content_rating,

        TRIM(genres) AS genres,

        PARSE_DATE('%B %e, %Y', last_updated) AS last_updated,

        TRIM(current_ver) AS current_ver,

        TRIM(android_ver) AS android_ver

    FROM source
    WHERE app != 'Life Made WI-Fi Touchscreen Photo Frame'

)

SELECT *,
    ROW_NUMBER() OVER (
        PARTITION BY app
        ORDER BY reviews DESC
    ) AS app_rank
FROM cleaned

