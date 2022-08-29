from django.db import models
# Create your models here.


class PrinterModelList(models.Model):
    name = models.CharField(max_length=200, unique=True,verbose_name='Модель принтера')
    def get_string_fields(self):
        return self.id, self.name
    def __str__(self):
        return self.name

class TonerModelList(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Модель картриджа')
    def get_string_fields(self):
        return self.id, self.name
    def __str__(self):
        return self.name


class PlacesList(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Площадка')
    def get_string_fields(self):
        return self.id, self.name
    def __str__(self):
        return self.name

class DepartmentList(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Отдел')
    def get_string_fields(self):
        return self.id, self.name
    def __str__(self):
        return self.name

DB_DCT_1 = {'printermodel': PrinterModelList, 'toner':TonerModelList,'places':PlacesList}
class PrintersMain(models.Model):
    ip = models.GenericIPAddressField(max_length=50, protocol='IPv4', unique=True, verbose_name='IP')
    printermodel = models.ForeignKey(PrinterModelList, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Модель принтера')
    toner = models.ForeignKey(TonerModelList, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Модель картриджа')
    place = models.ForeignKey(PlacesList, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Площадка')
    comment = models.CharField(max_length=200,verbose_name='Комментарий')
    def get_string_fields(self):
        return self.id, self.ip, self.printermodel, self.toner, self.place, self.comment
    def __str__(self):
        return self.ip

class DrumList(models.Model):
    name = models.CharField(max_length=200, unique=True,verbose_name='Драм')
    def get_string_fields(self):
        return self.id, self.name
    def __str__(self):
        return self.name

DB_DCT = {'printermodel': PrinterModelList, 'toner':TonerModelList,'places':PlacesList,'printers':PrintersMain,'department':DepartmentList,'drum':DrumList}

# printermodel = models.ForeignKey(PrinterModelList, on_delete=models.CASCADE, blank=True, null=True)
#     toner = models.ForeignKey(TonerModelList, on_delete=models.CASCADE, blank=True, null=True)
#     place = models.ForeignKey(PlacesList, on_delete=models.CASCADE, blank=True, null=True)