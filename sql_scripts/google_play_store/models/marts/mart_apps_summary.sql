SELECT

    a.app,

    a.category,

    a.app_type,

    a.rating,

    a.installs,

    a.price,

    a.reviews AS total_reviews,

    r.review_count AS sample_review_count,

    r.avg_sentiment,

    r.positive_review_pct,

    CASE
        WHEN a.price > 0 THEN TRUE
        ELSE FALSE
    END AS is_paid

FROM {{ ref('stg_apps') }} a

LEFT JOIN {{ ref('int_review_metrics_by_app') }} r
    ON a.app = r.app

WHERE a.app_rank = 1