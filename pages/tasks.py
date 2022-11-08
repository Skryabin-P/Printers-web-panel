
from __future__ import absolute_import,unicode_literals
# import django
# django.setup()
from interface.celery import shared_task
from admin_dashboard.models import PrintersMain
from pages.models import RequestPrinters,ObmenFolders
from func import get_full_info
from interface.celery import app
import os
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
<<<<<<< HEAD
            if previous_note != None:
                # if amount of toner now is bigger than previous amount then toner was changed
                if int(previous_note) >= 0:
                    if (int(temp_info['black_toner_left']) > (15 + int(previous_note.toner_left))) and (
                            int(temp_info['black_toner_left']) > 1):
                        changed = 1
=======
            if previous_note is not None:
                if previous_note.toner_left != None:
                    # if amount of toner now is bigger than previous amount then toner was changed
                    if int(previous_note.toner_left) >=0:
                        if (int(temp_info['black_toner_left']) > (15 + int(previous_note.toner_left))) and (int(temp_info['black_toner_left'] ) > 1):
                            changed = 1
>>>>>>> blyat



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

@app.task
def scan_obmen():
    all_dirs = os.listdir(fr'\\10.7.202.50\obmen')
    dirs = []
    for dir in all_dirs:
        if os.path.isdir(fr'\\10.7.202.50\obmen\{dir}'):
            dirs.append(dir)
    for dir in dirs:
        if len(ObmenFolders.objects.filter(name=dir)) == 0:
            db = ObmenFolders.objects.create(name=dir,description='Описание не добавлено')
            db.save()
    for folder in ObmenFolders.objects.all():
        if folder.name not in dirs:
            folder.delete()






#

