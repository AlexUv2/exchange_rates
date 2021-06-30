from PostgresDB import Postgresql
from config import Config
from datetime import datetime, timedelta
from Notification.my_email import Email
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def compare_rates(curr_pair: str, period: int) -> dict:
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

    e = Email(credentials=Config.EMAIL_CREDS)
    mid_rates = round(sum(rates['last_days_rates']) / len(rates['last_days_rates']), 3)

    subject = 'Currency rates'
    message = None
    if rates['today_rate'] > max(rates['last_days_rates']):
        message = f'''
                   <h2>Сегодня хороший курс для <b>продажи</b> доллара</h2>
                   <div>Средний курс за прошедшие {Config.PERIOD} дней:
                   <b color="red">{mid_rates}</b></div>
                   <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                   <b>График курса</b><img src="cid:{'plot'}" alt="График валют">
                   '''

    elif rates['today_rate'] < min(rates['last_days_rates']):
        message = f'''
                   <h2>Сегодня хороший курс для <b>покупки</b> доллара</h2>
                   <div>Средний курс за прошедшие {Config.PERIOD} дней:
                   <b color="red">{mid_rates}</b></div>
                   <div>Сегодняшний курс: <b color="blue">{rates['today_rate']}</b></div>
                   <b>График курса</b><img src="cid:{'plot'}" alt="График валют">
                   '''
    else:
        print('No good news to you')

    if message:
        e.send(to=Config.EMAIL_TO, message=message, subject=subject, is_html=True)


def plot_rates():
    pg = Postgresql(credentials=Config.DB_CREDS)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=12)

    sql = f"""
            select 
                avg(rate) as rate, 
                datetime::date
            from usd_uah
            where datetime::date between '{start_date}' and '{end_date}'
            group by datetime::date
            order by datetime;
        """

    last_week_rates = pg.get_rows(sql=sql, as_dict=True)
    df = pd.DataFrame(last_week_rates)
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.plot(df['datetime'], df['rate'])
    ax.set_ylabel('Курс')
    ax.set_xlabel('Дата')
    ax.xaxis.set_major_formatter(DateFormatter("%d.%m.%Y"))
    fig.autofmt_xdate()
    plt.xticks(df['datetime'])
    plt.savefig('plot.png')


def main():
    rates = compare_rates(period=Config.PERIOD, curr_pair=Config.CURRENCY_PAIR)
    plot_rates()
    email_send(rates=rates)


if __name__ == '__main__':
    main()
