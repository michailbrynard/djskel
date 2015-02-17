#!/bin/bash
export PGUSER=webrt
export PGDB=webrt
export PGPASSWORD=u1HMGMCSJprrebxh6Y9I
psql -U ${PGUSER} ${PGDB} -t -c "select 'drop table \"' || tablename || '\" cascade;' from pg_tables where schemaname = 'public'" | psql -U ${PGUSER} ${PGDB}
