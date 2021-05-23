from PostgresDB import Postgresql
from config import Config
from datetime import datetime, timedelta
from Notification.email import Email


# TODO:
# Add plots to email with rates for the last days


def compare_rates(curr_pair: str, period: int):
    """
    Compares data for the last 10 days
    """
    pg = Postgresql(credentials=Config.DB_CREDS)

    today = datetime.today()
    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=period)

    sql = f"""
            select 
                rate
            from {curr_pair.lower()}
            where datetime::date between '{start_date}' and '{end_date}';
        """
    last_days_rate = pg.get_column(sql=sql)

    sql = f"""
            select 
                rate
            from {curr_pair.lower()}
            where datetime::date = '{today}'
            order by datetime desc
            limit 1
        """
    today_rate = pg.get_column(sql=sql)

    if not last_days_rate or not today_rate:
        raise Exception('No values returned from exchange_rates DB')

    return {
        'last_days_rates': last_days_rate,
        'today_rate': today_rate[0]
    }


def email_send(rates: dict):
    subject = 'Currency rates'

    e = Email(credentials=Config.EMAIL_CREDS)

    message = None
    if rates['today_rate'] > max(rates['last_days_rates']):
        message = f'''
                   <h2>Сегодня хороший курс для <b>продажи</b> доллара</h2>
                   <div>Средний курс за прошедшие 10 дней: 
                   <b color="red">{round(sum(rates['last_days_rates']) / len(rates['last_days_rates']), 3)}</b></div>
                   <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                   '''

    elif rates['today_rate'] < min(rates['last_days_rates']):
        message = f'''
                   <h2>Сегодня хороший курс для <b>покупки</b> доллара</h2>
                   <div>Средний курс за прошедшие 10 дней: 
                   <b color="red">{round(sum(rates['last_days_rates']) / len(rates['last_days_rates']), 3)}</b></div>
                   <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                   '''
    else:
        print('No good news to you')

    if message:
        e.send(to=Config.EMAIL_TO, message=message, subject=subject, is_html=True)


def main():
    rates = compare_rates(period=10, curr_pair=Config.CURRENCY_PAIR)
    email_send(rates=rates)


if __name__ == '__main__':
    main()
