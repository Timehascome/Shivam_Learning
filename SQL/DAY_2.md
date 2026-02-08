**Concepts**
COUNT, SUM, AVG, MIN, MAX
GROUP BY
HAVING
DISTINCT

**Practice**
Employees per department
Departments with avg salary > X
Count distinct users per day
Difference between COUNT(*) vs COUNT(col)
Can HAVING be used without GROUP BY?
Why non-aggregated columns fail in SELECT?

>>select department,DATE_FORMAT(sale_date,'%Y-%m'),sum(sales_amount) as sum_sales from employee_sales group by department, DATE_FORMAT(sale_date, '%Y-%m');


