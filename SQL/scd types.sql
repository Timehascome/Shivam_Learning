-- SCD Type 1
merge into `project-bq-451206.bigquery_dataset.products` t 
using `project-bq-451206.bigquery_dataset.products_change` s
on t.product_id = s.product_id
when matched and (
  t.product_name <> s.product_name
  or t.price <> s.price
) then 
  update set 
    t.product_name = s.product_name,
    t.price = s.price,
    t.last_updated = s.last_updated
when not matched then 
  insert (product_id, product_name, category, price, last_updated) 
  values (s.product_id, s.product_name, s.category, s.price, s.last_updated);

  -- SCD Type 2

  -- Approach 1 (1 merge statement)
merge into `project-bq-451206.bigquery_dataset.products_scd2` t
using (
  select stg.product_id as join_key, stg.* from `project-bq-451206.bigquery_dataset.products_scd2_change` stg
  union all
  select null as join_key, stg.* 
    from `project-bq-451206.bigquery_dataset.products_scd2_change` stg
    join
    `project-bq-451206.bigquery_dataset.products_scd2` dim
    on stg.product_id = dim.product_id
    where dim.is_current = true and (stg.product_name != dim.product_name or stg.category != dim.category or stg.price != dim.price)
) s
on t.product_id = s.join_key and t.is_current = true

when matched and (
  t.product_name <> s.product_name
  or t.category <> s.category
  or t.price <> s.price
) then
  update set 
    t.is_current = false,
    t.end_date = s.start_date

when not matched then
  insert (product_id, product_name, category, price, start_date, end_date, is_current)
  values (s.product_id, s.product_name, s.category, s.price, s.start_date, null, true);