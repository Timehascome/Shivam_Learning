**Concepts**
SELECT, FROM
WHERE
AND / OR / NOT
IN, BETWEEN
LIKE, wildcards % _
IS NULL vs = NULL ❗

**Practice**
Filter customers with missing emails
Find orders between two dates
Case-insensitive search
Difference between WHERE and HAVING
Why NULL = NULL is false?
LIKE '%abc%' vs LIKE 'abc%'
When does BETWEEN become dangerous?
>>BETWEEN is dangerous when used on DATETIME or TIMESTAMP columns because it is inclusive and truncates time to midnight, silently excluding valid rows.
WHERE salary > 50000 OR bonus IS NOT NULL
>>Explain operator precedence?? 
Answer : First comparision takes precedence (salary>50000)  (bonus IS NOT NULL); Then OR is applied 

**Order of SQL Clause Execution (Very Important – Different from precedence!)**
1. FROM
2. JOIN
3. WHERE
4. GROUP BY
5. HAVING
6. SELECT
7. DISTINCT
8. ORDER BY
9. LIMIT / OFFSET

>>Precedence ≠ execution order:
In SQL, order of precedence defines which operations are evaluated first when multiple operators appear in a single expression (especially in WHERE, JOIN ON, HAVING, and SELECT expressions).
Precedence Order:
================
Parentheses ()
Unary  -salary , +salary
Multiply/Divide  * /
Add/Subtract   + -
Comparison     [=  <>   !=   >   <   >=   <=] "BETWEEN" / "IN" /"LIKE" / "IS [NOT] NULL"
NOT
AND
OR

