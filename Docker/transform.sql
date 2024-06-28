.mode csv
.import /extract/yellow_tripdata_2024-01.partial.csv yellow_tripdata_2024_01
.header on

drop table if exists passenger_amount;
create table passenger_amount (passengers int, amount float);

# select relevant data from extracted and imported data
insert into passenger_amount
  select passenger_count as passenger, total_amount as amount
  from yellow_tripdata_2024_01
  where passenger_count > 2 and total_amount > 0 ;

# drop the imported table as we do not need it any longer
drop table yellow_tripdata_2024_01;

# our transformed data is in table passenger_amount