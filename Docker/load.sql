.mode csv
.header on

select sum(passengers) from passenger_amount;

.output /load/load.csv
select sum(passengers) from passenger_amount;