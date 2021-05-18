-- comment1
-- comment2

create table employee
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2)
);

insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);



insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);


/********
  some block comment
 */



insert into employee values(2008, 'Max', 'Powers', 'M', 'Sales Representative', 2, 59000);
insert into employee values(2009, 'Stacy', 'Jacobs', 'F', 'Sales manager', 2, 730000);
insert into employee values(2010, 'John', 'Henery', 'M', 'Sales director', 2, 90000);

----- return employee record with max salary
select
*
from employee e
order by e.salary desc
limit 1
;

-- return higherst salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;


-- select 2nd highest salary in employee table

select
ranked_salary.salary
from
(
	select
	e.salary,
	e.first_name,
	dense_rank() over (order by e.salary desc) as salary_rank
	from employee e
) ranked_salary
where ranked_salary.salary_rank = 2
;