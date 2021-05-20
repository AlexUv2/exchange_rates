#TODO:
# Наладить нотификейшн
# Структура проекта 3-4 файла
# Сделать класс для этой бд

from config import Config
from PostgresDB import Postgresql
from RatesAPI import RatesAPI


def check_or_create_table(curr_pair: str):
    """ СДЕЛАТЬ МЕТОДОМ КЛАССА БАЗЫ ДАННЫХ"""
    pg = Postgresql(credentials=Config.credentials)

    sql = """
            select 
                table_name 
            from information_schema.tables  
            where table_schema='public';
        """

    tables = pg.get_column(sql=sql)
    if curr_pair.lower() in tables:
        return

    sql_create = f"""
                    create table {curr_pair.lower().strip()}( 
                        id serial primary key, 
                        rate float8 not null, 
                        datetime timestamp not null default NOW() 
                    );
                 """
    pg.exec(sql=sql_create)


def main():
    currency_pair = 'usd_eur'

    pg = Postgresql(credentials=Config.credentials)
    r = RatesAPI(token=Config.token)

    check_or_create_table(curr_pair=currency_pair)

    rates = r.get_rate(curr_pair=currency_pair)
    if rates:
        sql = f'insert into {currency_pair.lower()}(rate) values ({rates[currency_pair.upper()]})'
        pg.exec(sql=sql)


if __name__ == '__main__':
    main()
