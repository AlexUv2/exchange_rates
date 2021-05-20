# exchange_rates
Python script for detecting the best course for the last 30 days


db structure: 
create table uah_usd( 
       id serial primary key, 
       rate float8 not null, 
       datetime timestamp not null default NOW()
       );
