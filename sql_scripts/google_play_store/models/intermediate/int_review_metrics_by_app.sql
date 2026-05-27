SELECT

    app,

    COUNT(*) AS review_count,

    AVG(sentiment_polarity) AS avg_sentiment,

    AVG(sentiment_subjectivity) AS avg_subjectivity,

    COUNTIF(sentiment = 'Positive') / COUNT(*)
        AS positive_review_pct

FROM {{ ref('stg_reviews') }}

GROUP BY app