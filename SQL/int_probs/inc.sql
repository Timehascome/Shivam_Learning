WITH incremental_data AS (
    SELECT *
    FROM source_orders
    WHERE updated_at > (
        SELECT COALESCE(MAX(updated_at), '1900-01-01')
        FROM target_orders
    )
),

deduped AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY order_id
               ORDER BY updated_at DESC
           ) AS rn
    FROM incremental_data
)

MERGE INTO target_orders t
USING (SELECT * FROM deduped WHERE rn = 1) s
ON t.order_id = s.order_id

WHEN MATCHED THEN UPDATE SET
    t.amount = s.amount,
    t.updated_at = s.updated_at

WHEN NOT MATCHED THEN INSERT *
;