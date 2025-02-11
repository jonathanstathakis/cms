-- get the relevent table names
create temp table table_names as
select table_name
from duckdb_tables;
from table_names;
-- get the column data
-- create temp table columns as
-- select 
create temp table columns as
select a.table_name,
    column_name,
    comment,
    column_default,
    is_nullable,
    data_type
from duckdb_columns a
    JOIN table_names b ON a.table_name = b.table_name;
-- constraints
create temp table constraints as
select a.table_name,
    constraint_text,
    constraint_column_names
from duckdb_constraints a
    JOIN table_names b on a.table_name = b.table_name;
from table_names;
from columns;
from constraints;