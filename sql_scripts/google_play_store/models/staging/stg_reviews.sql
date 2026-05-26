WITH source AS (

    SELECT *
    FROM {{ source('raw', 'raw_reviews') }}

),

cleaned AS (

    SELECT

        TRIM(app) AS app,

        NULLIF(TRIM(translated_review), '') AS translated_review,

        INITCAP(sentiment) AS sentiment,

        SAFE_CAST(sentiment_polarity AS FLOAT64)
            AS sentiment_polarity,

        SAFE_CAST(sentiment_subjectivity AS FLOAT64)
            AS sentiment_subjectivity

    FROM source

)

SELECT *
FROM cleaned
WHERE translated_review IS NOT NULL