Subqueries & CTEs

Goal: Think in layers
Concepts
Subqueries in SELECT, WHERE, FROM
Correlated subqueries   >> tricky need practice 
WITH (CTE)
Recursive CTE (basic idea)

Interview Questions
Subquery vs CTE
When does correlated subquery run?
Performance implications

Practice
Salary > department avg
Latest record per user
Remove duplicates

Must-Know Trap
WHERE salary > (SELECT AVG(salary) FROM emp)
↳ Explain evaluation order
**Correlated subqueries**
SELECT *
FROM emp e
WHERE salary >
(
  SELECT AVG(e2.salary)
  FROM emp e2
  WHERE e2.dept_id = e.dept_id
);
