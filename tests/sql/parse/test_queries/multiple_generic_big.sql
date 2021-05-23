


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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
select
max(e_max.salary) as highes_salary
from employee e_max;



select 1 from oneliner_query;


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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */




drop table if exists all_datatypes;
create table if not exists all_datatypes(
	-- ---------------------------
	-- NUMERIC TYPES
	-- ---------------------------

	-- integers
	f_smallint smallint, -- signed 2 bytes
	f_integer integer, -- signed 4 bytes
	f_bigint bigint, -- signed 8 bytes

	-- decimals
	f_decimal decimal,
	f_decimal_15_5 decimal(15, 5),
	f_decimal_15_0 decimal(15, 0),
	f_decimal_15 decimal(15), -- default scale = 0
	f_numeric numeric,

	-- floating points
	f_real real,
	f_double double precision,

	-- serials
	f_smallserial smallserial, -- bytes -- range only [1: +] but upper range as unsigned int types
	f_serial serial, -- 4 bytes
	f_bigserial bigserial, -- 8 bytes

	-- money
	f_money money,

	-- boolean
	f_boolean boolean,

	-- ---------------------------
	-- CHARACTER TYPES
	-- ---------------------------
	f_char_50 char(50), -- character(x) bpchar?
	f_char char, -- char(1)
	f_varchar_50 varchar(50), -- character varying
	f_varchar varchar,
	f_text text,

	-- ---------------------------
	-- DATE TIME TYPES
	-- ---------------------------
	-- p [0, 6] stands for precision, it is number of fractional digits retained in the seconds field. 0 when not specified
	-- when no WITH TIME ZONE is specified then it is [WITHOUT TIME ZONE]
	f_timestamp timestamp, -- bytes
	f_timestamp_0 timestamp(0),
	f_timestamp_6 timestamp(6),
	f_timestamp_wts timestamp with time zone,
	f_timestamp_0_wts timestamp(0) with time zone,
	f_timestamp_6_wts timestamp(6) with time zone,

	f_date date, -- 4 bytes - 1 day resolution

	f_time time, -- bytes
	f_time_0 time(0),
	f_time_6 time(6),
	f_time_wts time with time zone,
	f_time_0_wts time(0) with time zone,
	f_time_6_wts time(6) with time zone,

	-- intervals
	f_interval_year interval year,
	f_interval_month interval month,
	f_interval_day interval day,
	f_interval_hour interval hour,
	f_interval_minute interval minute,
	f_interval_second interval second, -- precision available [p]
	f_interval_year_to_month interval YEAR TO month,
	f_interval_day_to_hour interval DAY TO hour,
	f_interval_day_to_minute interval DAY TO minute,
	f_interval_day_to_second interval DAY TO second, -- p
	f_interval_hour_to_minute interval HOUR TO minute,
	f_interval_hour_to_second interval HOUR TO second ,-- p
	f_interval_minute_to_second interval MINUTE TO second --p

);





-- based on:
-- https://www.youtube.com/watch?v=uAWWhEA57bE&list=WL&index=38&t=145s

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

create table department
(
	department_id int primary key,
	department_name varchar(50)
);


alter table employee add constraint employee_department_fk
foreign key (department_id) references department (department_id);

insert into department values (1,'IT');
insert into department values (2,'Sales');


insert into employee values(2002, 'Super', 'Man', 'M', 'Tester', 1, 75000);
insert into employee values(2003, 'Jessica', 'lyers', 'F', 'Architect', 1, 60000);
insert into employee values(2004, 'Bonnie', 'Adams', 'F', 'Project Manager', 1, 80000);
insert into employee values(2005, 'James', 'Madison', 'M', 'Sodtware developer', 1, 55000);
insert into employee values(2006, 'Michael', 'Greenback', 'M', 'Sales Assistant', 2, 85000);
insert into employee values(2007, 'Leslie', 'Peters', 'F', 'Sales engineer', 2, 76000);
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


select
*
from employee e
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest salary in employee table
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


-- select range of employee based on id  ???
select
*
from employee e
where e.employee_id between 2005 and 2007;


-- return an amployee with highest salary and employees department name

select
e.*,
d.department_name
from employee e
left join department d
on e.department_id = d.department_id
where e.salary = (select max(e_max.salary) from employee e_max)
;


-- return highest slary, employee_name, department_name for each department

select
d.department_name,
max(e.salary) highest_salary
from employee e
left join department d
on e.department_id = d.department_id
group by d.department_name;


select * from employee


drop table test2;
create table test2
(
	employee_id int primary key,
	first_name varchar(50),
	last_name varchar(100),
	gender varchar(1),
	position varchar(50),
	department_id int,
	salary numeric(9,2),
	text_field text,
	interval
);


/***
  some block comment
 */

