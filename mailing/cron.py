import smtplib
from datetime import datetime, timedelta
from calendar import monthrange
from mailing.models import Mailing, Log
from mailing.services import send_mailing


def start_mailing():
    """Функция проверки и начала рассылок"""
    now = datetime.now()
    mailing_list = Mailing.objects.filter(date__lte=now, time__lte=now, status='created')

    for mailing in mailing_list:
        user = mailing.user
        mailing.status = 'started'
        mailing.save()

        clients = mailing.client.all()
        message = mailing.message
        try:
            response = send_mailing(clients, message)

            log = Log.objects.create(time=now, status=bool(response), server_response='', mailing=mailing,
                                     user=user)
            mailing.status = 'created'
            if mailing.periodisity == 'day':
                mailing.date += timedelta(days=1)
            elif mailing.periodisity == 'week':
                mailing.date += timedelta(weeks=1)
            elif mailing.periodisity == 'month':
                month = now.month
                year = now.year
                days_count = monthrange(year, month)
                mailing.date += timedelta(days=days_count[1])
        except smtplib.SMTPException as e:
            log = Log.objects.create(time=now, status=bool(response), server_response=e, mailing=mailing,
                                     user=user)
            mailing.status = 'created'
        finally:
            log.save()
            mailing.save()
