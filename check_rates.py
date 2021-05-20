from PostgresDB import Postgresql
from config import Config
from datetime import datetime, timedelta
from notify.email import Email
#TODO: Добавить график курса за последние дни


def compare_rates(curr_pair: str, period: int):
    """
    Сравнивает даныне за последние 10 дней с сегодняшним курсом
    :return:
    """
    pg = Postgresql(credentials=Config.credentials)

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
        message = f'''<h2>Сегодня хороший курс для <b>продажи</b> доллара</h2>
                      <div>Средний курс за прошедшие 10 дней: 
                      <b color="red">{round(sum(rates['last_days_rates']) / len(rates['last_days_rates']), 3)}</b></div>
                      <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                      '''

    if rates['today_rate'] < min(rates['last_days_rates']):
        message = f'''<h2>Сегодня хороший курс для <b>покупки</b> доллара</h2>
                      <div>Средний курс за прошедшие 10 дней: 
                      <b color="red">{round(sum(rates['last_days_rates']) / len(rates['last_days_rates']), 3)}</b></div>
                      <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                      '''
    if message:
        e.send(to=Config.EMAIL_TO, message=message, subject=subject, is_html=True)


def main():
    rates = compare_rates(period=10, curr_pair='usd_uah')
    email_send(rates=rates)


if __name__ == '__main__':
    main()
