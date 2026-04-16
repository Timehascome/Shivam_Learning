--position/substring_index in sql
SELECT email,
    -- fname
    SUBSTRING_INDEX(SUBSTRING_INDEX(email, '@', 1), '.', 1) AS fname,
    -- mname
    CASE WHEN LENGTH(SUBSTRING_INDEX(email, '@', 1)) - LENGTH(REPLACE(SUBSTRING_INDEX(email, '@', 1), '.', '')) = 2
        THEN SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(email, '@', 1), '.', 2),'.',-1) ELSE NULL END AS mname,
    -- lname
    SUBSTRING_INDEX(SUBSTRING_INDEX(email, '@', 1), '.', -1) AS lname
FROM your_table; 


--unpivot in pyspark/sql  --needs hands on 
--india,pakistan,bangladesh,nepal;  --self join 
--bowler_id, over_number, ball_number, runs_scored (W/1/2/3/4/5/6);
#python tricky
--maximum toys can be bought with given money and price of each toy
--input: money, price of each toy

