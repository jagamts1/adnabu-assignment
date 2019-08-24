from __future__ import absolute_import, unicode_literals
from zipsender.api.v1.custom_modules import DataProcess
from celery import shared_task


@shared_task
def send_to_mail(data=None):
    obj = DataProcess(data.get('email'), data.get('urls'))
    obj.download_html().make_zip().send_zip()
