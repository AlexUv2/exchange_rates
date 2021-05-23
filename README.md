### exchange_rates
Python script for detecting the best exchange rate for the last 10 days


###How to start it:
 1. Clone the project
 2. Add to the project file 'config.py' with he following structure and fill it:
 
        class Config:
        TOKEN = <'str: token'>
        # You can use my token ff4fbcb96cfe793d9e47
        
        CURRENCY_PAIR = 'usd_uah'

        DB_CREDS = {
            'dbname': <'str: db_name'>,
            'user': <'str: db_username'>,
            'password': <' str: db_password'>,
            'host': <'str: db_host'>
        }

        EMAIL_TO = <'str: email_to'>

        EMAIL_CREDS = {
            'login': <'str: email_from_'>,
            'password': <'str: email_password'>,
            'port': 465, # default port for smtp
            'host': 'smtp.gmail.com' # default smtp host for gmail. Change it for anothe emails
        }

  3. Create PostgreSQL database or add exciting database credentials to 'config.py'
  4. Set to autorun data_collection.py and check_rates.py
  5. Waif row about a week for some data to have results


    table structure: 
    create table usd_uah( 
           id serial primary key, 
           rate float8 not null, 
           datetime timestamp not null default NOW()
           );




#### Plans for future:
 1. Add plots to email for seeing how rates changed.
 2. Add a prediction model for each currency pairs.
 3. Add ability to process data for more currency pairs.
    