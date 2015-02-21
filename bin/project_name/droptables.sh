#!/bin/bash
export PGUSER={{ project_name }}
export PGDB={{ project_name }}
export PGPASSWORD={{ secret_key }}

pg_dump -U ${PGUSER} ${PGDB} -f database_dump.sql

psql -U ${PGUSER} ${PGDB} -t -c "select 'drop table \"' || tablename || '\" cascade;' from pg_tables where schemaname = 'public'" | psql -U ${PGUSER} ${PGDB}

#pg_dump -U ${PGUSER} -d ${PGDB} -f database_dump.sql