from django.db import models
from admin_dashboard.models import DB_DCT
from django.contrib.auth.models import User
class GiveCartridge(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    printermodel = models.ForeignKey(DB_DCT['printermodel'], on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Модель принтера')
    toner = models.ForeignKey(DB_DCT['toner'], on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Модель картриджа')
    place = models.ForeignKey(DB_DCT['places'], on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Площадка')
    department = models.ForeignKey(DB_DCT['department'], on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Отдел')
    amount = models.IntegerField(verbose_name='Количество', default=1)
    comment = models.CharField(max_length=200, verbose_name='Комментарий', blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Выдано(кем)')
    def get_string_fields(self):
        return self.id, self.date, self.printermodel, self.toner, self.place, self.department, self.amount, self.comment, self.issued_by
    # def __str__(self):
    #     return self.id

class GiveDrum(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    printermodel = models.ForeignKey(DB_DCT['printermodel'], on_delete=models.CASCADE, blank=True,null=True,
                                     verbose_name='Модель принтера')
    drum = models.ForeignKey(DB_DCT['drum'], on_delete=models.CASCADE, blank=True,null=True, verbose_name='Модель драма')
    place = models.ForeignKey(DB_DCT['places'], on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Площадка')
    department = models.ForeignKey(DB_DCT['department'], on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Отдел')
    comment = models.CharField(max_length=200, verbose_name='Комментарий', blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Выдано(кем)')
    def get_string_fields(self):
        return self.id, self.date, self.printermodel, self.drum, self.place, self.department, self.comment, self.issued_by


class RequestPrinters(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    printer = models.ForeignKey(DB_DCT['printers'], on_delete=models.CASCADE, blank=True, null=True, verbose_name='')
    page_utility = models.IntegerField(verbose_name='Страниц отпечатано',)
    toner_left = models.IntegerField( verbose_name='Осталось тонера')
    device_name = models.CharField(max_length=200, verbose_name='Сетевое имя')
    changed = models.IntegerField(blank=True, null=True)
    def get_string_fields(self):
        return self.id, self.date, self.printer,  self.page_utility, \
               self.toner_left, self.device_name, self.changed


