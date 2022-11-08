
from __future__ import absolute_import,unicode_literals
# import django
# django.setup()
from interface.celery import shared_task
from admin_dashboard.models import PrintersMain
from pages.models import RequestPrinters
from func import get_full_info
from interface.celery import app
@shared_task
def add(x,y):
    return x+y

@app.task
def request_printers():
    for printer in PrintersMain.objects.all():
        temp_info = get_full_info(printer.ip)
        if temp_info['pages'] != None:

            previous_note = RequestPrinters.objects.filter(printer=printer).last()

            changed = 0
            if previous_note is not None:
                if previous_note.toner_left != None:
                    # if amount of toner now is bigger than previous amount then toner was changed
                    if int(previous_note.toner_left) >=0:
                        if (int(temp_info['black_toner_left']) > (15 + int(previous_note.toner_left))) and (int(temp_info['black_toner_left'] ) > 1):
                            changed = 1



                db = RequestPrinters.objects.create(printer = printer,page_utility=temp_info['pages'],
                                                    toner_left = temp_info['black_toner_left'],device_name=temp_info['Device name'],
                                                    changed=changed)
                db.save()
            else:
                db = RequestPrinters.objects.create(printer=printer, page_utility=temp_info['pages'],
                                                    toner_left=temp_info['black_toner_left'],
                                                    device_name=temp_info['Device name'],
                                                    changed=changed)
                db.save()



#

