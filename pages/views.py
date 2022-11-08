import datetime

from django.shortcuts import render,redirect
from django.http import HttpResponse, FileResponse
from django.db.models import Q, Min, Max, Sum,F, Case, When,Value,FloatField,CharField,Subquery, OuterRef
from django.db.models.functions import Coalesce
from .models import GiveCartridge,RequestPrinters, GiveDrum,ObmenFolders
from django.views.generic.edit import DeleteView,CreateView, UpdateView
from admin_dashboard.models import PlacesList, PrintersMain
from django.views.generic.list import ListView
from func import get_full_info
from django.forms.models import model_to_dict
<<<<<<< HEAD
from .forms import GiveCartridgeForm,TonerUtilsFilter,CartridgeFilter,RequestFilter,GiveDrumForm,DrumFilter,RequestFilterTest
=======
from .forms import GiveCartridgeForm,TonerUtilsFilter,CartridgeFilter,RequestFilter,GiveDrumForm,DrumFilter,ObmenForms
>>>>>>> blyat
from django.urls import reverse
from django.core.paginator import Paginator
import xlwt
from django.core import serializers
from django.shortcuts import get_object_or_404

from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


class Main(ListView):
    template_name = 'home.html'
    model = PlacesList
    context_object_name = 'places'

# check status and info about printers in live mode
def printerstats(response, place):
    where = PlacesList.objects.get(name=place)
    printers = PrintersMain.objects.filter(place=where).all()
    printers_output = []
    header1 = ['ip','comment']

    dict2 = {}
    if len(printers) > 0:
        for item in printers:
            model = item.printermodel.name
            item = model_to_dict(item)


            temp_dict = {}
            for h in header1:
                dict2[h] = dict(item)[h]
            temp_dict.update(dict2)
            req_printer = get_full_info(item['ip'],model)
            temp_dict.update(req_printer)
            if temp_dict['pages'] != None:
                temp_dict['status'] = 'Online'
            else:
                temp_dict['status'] = 'Offline'
            printers_output.append(temp_dict)
        header = list(printers_output[0].keys())


        return render(response,'printerstats.html',context={'printers':printers_output,'header':header})

    else:
        error = f"There's no printers yet. Add printers for {place}"
        return render(response, 'printerstats.html', context={'error': error})



def cartridge_stats(response):
    # stats of how many cartridges(toners) was gived to departments
    fields = [f.verbose_name for f in GiveCartridge._meta.fields]

    filter = CartridgeFilter(response.GET, queryset=GiveCartridge.objects.all().order_by('-date','-pk'))
    context = {}
    context['filter'] = filter
    context['q'] = filter.qs.values("date", "printermodel__name","toner__name",
                                    "place__name","department__name","amount","comment","issued_by__username")
    eng_fields = ["date", "printermodel__name","toner__name",
                                    "place__name","department__name","amount","comment","issued_by__username"]

    context['fields'] = fields  # fields name in russian
    context['eng_fields'] = eng_fields
    paginated_set = Paginator(filter.qs, 20)
    page_number = response.GET.get('page')
    page_obj = paginated_set.get_page(page_number)
    context['page_obj'] = page_obj
    date_min = response.GET.get('date_min')
    date_max = response.GET.get('date_max')

    # dates for export in excel
    if date_min == None or date_min == '':
        date_min = '---'
    if date_max == None or date_max == '':
        date_max = '---'
    if str(response.GET.get('export')) == '1':
        return export_toner_withdraw(response, context, date_min,date_max)


    return render(response,'cartridge_withdraw.html',context=context)


def drum_stats(response):
    # similarly with cartridge_stats
    fields = [f.verbose_name for f in GiveDrum._meta.fields]

    filter = DrumFilter(response.GET, queryset=GiveDrum.objects.all().order_by('-date','-pk'))
    context = {}
    context['filter'] = filter

    context['fields'] = fields
    paginated_set = Paginator(filter.qs, 20)
    page_number = response.GET.get('page')
    page_obj = paginated_set.get_page(page_number)
    context['page_obj'] = page_obj


    return render(response,'drum_withdraw.html',context=context)


def request_printers_stats(response):
    # test view func to see all records in table RequestPrinters
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.name for f in RequestPrinters._meta.fields]
    # form = ChooseCategoryForm
    filter = RequestFilterTest(response.GET, queryset=RequestPrinters.objects.all().order_by('-date'))
    context = {}
    context['filter'] = filter
    context['fields'] = fields
    paginated_set = Paginator(filter.qs, 20)
    page_number = response.GET.get('page')
    page_obj = paginated_set.get_page(page_number)
    context['page_obj'] = page_obj
    return render(response,'cartridge_withdraw.html',context=context)

@query_debugger
def view_full_report(response):
    # to see all stats for each printer
    filter = RequestFilter(response.GET, queryset=RequestPrinters.objects.order_by())
    context = {}
    # annotate filtered queryset for each printer
    q = filter.qs.values("printer").annotate(ip = F('printer__ip'),
                                                        printer_model = F('printer__printermodel__name'), toner_model = F('printer__toner__name'),
                                                        place = F('printer__place__name'),
                                                        num_pages = (Max('page_utility') - Min('page_utility')),
                                                        cartridges = Sum('changed'),mean = Coalesce(Subquery(filter.qs.values('printer').filter(changed = 1, printer_id = OuterRef('printer_id')).annotate(cartridges=Sum('changed'), mean_per_cartridge=Case(
        When(cartridges__gt=1,changed=1, then=((Max('page_utility') - Min('page_utility')) / (F('cartridges')-1))),
        output_field=CharField())).values("mean_per_cartridge")), Value('Замены не было')), device_name = F('device_name'),
                                                        comment= F('printer__comment'))

    if len(q) > 0:
        fields = [f for f in q[0].keys()]
        ru_fields = ['ID','IP','Модель принтера','Модель картриджа','Площадка',
                     'Страниц отпечатано','Картриджей использовано','Ср. кол-во стр. на 1 картридж','Сетевое имя','Комментарий']
        context['fields'] = fields
        context['ru_fields'] = ru_fields
    else:
        error = "Nothing was found"
        context['error'] = error
    context['filter'] = filter
    paginated_set = Paginator(q, 20)
    page_number = response.GET.get('page')
    date_min = response.GET.get('date_min')
    date_max = response.GET.get('date_max')
    # dates for execl export
    if date_min == None or date_min =='':
        date_min = '---'
    if date_max == None or date_max =='':
        date_max = '---'
    page_obj = paginated_set.get_page(page_number)
    context['page_obj'] = page_obj
    if str(response.GET.get('export')) == '1':
        return export_excel(response, q, date_min,date_max)

    return render(response,'full_stats.html',context=context)
def give_cartridge(response):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    # view where you give toner , select printer model, toner model etc
    class CreateMyView(CreateView):
        model = GiveCartridge
        template_name = 'cartridgeform.html'
        form_class = GiveCartridgeForm
        success_url = f"/cartridge_stats"

        def get_initial(self):
            # set initial for field "issued_by" as logged user's ID
            self.initial.update({
                'issued_by': self.request.user.id,

            })
            return super(CreateMyView, self).get_initial()

    return CreateMyView.as_view()(response)

def give_drum(response):
    # similarly with give_cartridge
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")

    class CreateMyView(CreateView):
        model = GiveDrum
        template_name = 'cartridgeform.html'

        form_class = GiveDrumForm
        success_url = f"/drum_stats"

        def get_initial(self):

            self.initial.update({
                'issued_by': self.request.user.id,

            })
            return super(CreateMyView, self).get_initial()

    return CreateMyView.as_view()(response)




def delete_data(response,pk):
    # delete record from GiveCartridge
    if not response.user.is_authenticated:
        return redirect(f"/cartridge_stats")

    class DeleteParams(DeleteView):
        template_name = 'delete.html'
        model = GiveCartridge
        context_object_name = 'params'
        fields = [f.verbose_name for f in GiveCartridge._meta.fields]
        extra_context = {'fields':fields}
        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
            return obj
        def get_success_url(self):
            return reverse('cartridge_stats')


    return DeleteParams.as_view()(response)


def update_data(response, pk):
    # update record from GiveCartridge
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in GiveCartridge._meta.fields]
    class UpdateParams(UpdateView):
        template_name = 'update.html'
        model = GiveCartridge
        context_object_name = 'params'
        form_class = GiveCartridgeForm

        success_url = f"/cartridge_stats"

        extra_context = {'fields':fields}

        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)

            self.obj = queryset.get()

            return self.obj
        def get_success_url(self):
            return reverse('cartridge_stats')

    return UpdateParams.as_view()(response)

def delete_drum(response,pk):
    # delete record from GiveDrum
    if not response.user.is_authenticated:
        return redirect(f"/drum_stats")

    class DeleteParams(DeleteView):
        template_name = 'delete.html'
        model = GiveDrum
        context_object_name = 'params'
        fields = [f.verbose_name for f in GiveDrum._meta.fields]
        extra_context = {'fields':fields}
        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
            return obj
        def get_success_url(self):
            return reverse('drum_stats')


    return DeleteParams.as_view()(response)


def update_drum(response, pk):
    # update record from GiveDrum
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in GiveDrum._meta.fields]
    class UpdateParams(UpdateView):
        template_name = 'update.html'
        model = GiveDrum
        context_object_name = 'params'
        form_class = GiveDrumForm

        success_url = f"/drum_stats"

        extra_context = {'fields':fields}

        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            self.obj = queryset.get()

            return self.obj
        def get_success_url(self):
            return reverse('drum_stats')

    return UpdateParams.as_view()(response)


def export_excel(request, obj,date_min = False,date_max=False):
    if not request.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    return_obj = HttpResponse(content_type='application/vnd.ms-excel')
    top_row = 1
    bottom_row = 3
    left_column = 0
    right_column = 6
    fields = [ 'ip','printer_model', 'toner_model', 'device_name', 'num_pages', 'cartridges','mean']
    ru_fields = ['IP','Модель принтера','Модель картриджа','Сетевое имя','Страниц отпечатано','Картриджей использовано','Ср. кол-во стр. на 1 картридж']
    return_obj['Content-Disposition'] = 'attachment; filename=printer_report.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Report')
    row_num = 0
    column_style = xlwt.XFStyle()
    column_style.font.bold = True
    header_style = xlwt.easyxf("pattern: pattern solid, fore_color yellow; font: height 600, name Times New Roman"
                               ", color red; align: horiz center;")
    main_style = xlwt.XFStyle()
    obj = obj.order_by('place')
    places = set(dic['place'] for dic in obj) # unique places
    places = list(places)
    places.sort()

    for col in range(len(ru_fields)):
        if col ==0 or 3 <= col <=4:
            ws.col(col).width = 256 * 20

        else:
            ws.col(col).width = 256 * 32
        ws.write(row_num,col,ru_fields[col],column_style)

    # write in cell starts and end dates of the report
    ws.write(row_num,len(fields)+1,"Начало периода",column_style)
    ws.write(row_num, len(fields) + 2, "Конец периода", column_style)
    if date_min:
        ws.write(1,len(fields)+1,date_min,column_style)
        ws.col(len(fields)+1).width = 256 * 17
    if date_max:
        ws.write(1, len(fields) + 2, date_max, column_style)
        ws.col(len(fields) + 2).width = 256 * 17
    row_num = 0

    for place in places:
        ws.write_merge(top_row + row_num, bottom_row + row_num, left_column, right_column, place, style=header_style)
        row_num = bottom_row + row_num
        for row in obj:

            if row['place'] == place:
                row_num += 1
                for col in range(len(fields)):

                    ws.write(row_num, col, row[fields[col]], main_style)

    wb.save(return_obj)
    return return_obj

@query_debugger
def cartridge_utility(response):

    # Report with toner utility, when toner was changed , how many pages was printed,etc
    filter = TonerUtilsFilter(response.GET, queryset=RequestPrinters.objects.prefetch_related("printer").order_by())
    context = {}
    context['filter'] = filter
    context['fields'] = ["printer__ip","device_name","printer__comment","printer__printermodel","printer__toner","printer__place"]
    context['ru_fields1'] = ["IP","Сетевое имя","Комментарий","Модель принтера","Модель картриджа","Площадка"]
    context['ru_fields2'] = ["Дата установки","Дата замены","Количество страниц"]
    printers = filter.qs.filter(changed=1).values_list('printer',flat=True).distinct()

    stats_table = []
    info_table = []
    for printer in printers:
        group = []

        info = filter.qs.filter(changed=1,printer=printer).values("printer__ip","device_name","printer__comment","printer__printermodel__name","printer__toner__name","printer__place__name","page_utility","date")
        if len(info) > 1:
            sub_head = info[0].copy()
            sub_head.pop('page_utility')
            sub_head.pop('date')

            info_table.append(sub_head)
            temp_table = []
            for change_id in range(len(info)-1):
                infoset = {}

                diff = info[change_id + 1]['page_utility'] - info[change_id]['page_utility']
                date_changed = info[change_id + 1]['date']
                date_set = info[change_id]['date']
                infoset['date_set'] = date_set
                infoset['date_changed'] = date_changed
                infoset['diff'] = diff
                group.append(infoset)

            stats_table.append(group)
        else:
            pass





    paginated_set = Paginator(stats_table, 20)
    page_number = response.GET.get('page')
    page_obj = paginated_set.get_page(page_number)
    context['stats_table'] = stats_table
    context['page_obj'] = page_obj
    context['info_table'] = info_table
    context['range'] = range(len(info_table))
    date_min = response.GET.get('date_min')
    date_max = response.GET.get('date_max')
    if date_min == None or date_min == '':
        date_min = '---'
    if date_max == None or date_max == '':
        date_max = '---'
    if str(response.GET.get('export')) == '1':
        return export_toner(response, context, date_min,date_max)
    return render(response, 'cartridgestats.html', context=context)


def export_toner(request, context,date_min = False,date_max=False):
    if not request.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    return_obj = HttpResponse(content_type='application/vnd.ms-excel')
    top_row = 0
    bottom_row = 2
    left_column = 0
    right_column = 4
    info_table = context['info_table']
    stats_table = context['stats_table']
    fields1 = list(info_table[0].keys())
    fields2 = list(stats_table[0][0].keys())
    print(fields2)
    fields1.remove('printer__place__name')
    ru_fields1 = context['ru_fields1']
    ru_fields1.remove('Площадка')
    ru_fields2 = context['ru_fields2']
    return_obj['Content-Disposition'] = 'attachment; filename=toner_report.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Report')
    row_num = 0
    # date_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY/')
    column_style = xlwt.XFStyle()
    column_style.font.bold = True
    header_style = xlwt.easyxf("pattern: pattern solid, fore_color yellow; font: height 600, name Times New Roman"
                               ", color red; align: horiz center;")
    main_style = xlwt.XFStyle()
    # write in cell starts and end dates of the report
    ws.write(row_num, len(fields1) + 1, "Начало периода", column_style)
    ws.write(row_num, len(fields1) + 2, "Конец периода", column_style)
    if date_min:
        ws.write(1, len(fields1) + 1, date_min, column_style)
        ws.col(len(fields1) + 1).width = 256 * 17
    if date_max:
        ws.write(1, len(fields1) + 2, date_max, column_style)
        ws.col(len(fields1) + 2).width = 256 * 17

    places = set(dic['printer__place__name'] for dic in info_table) # unique places
    places = list(places)
    places.sort()
    print(places)

    for place in places:
        ws.write_merge(top_row + row_num, bottom_row + row_num, left_column, right_column, place, style=header_style)
        row_num = bottom_row + row_num+1

        for i in range(len(info_table)):

            if info_table[i]['printer__place__name'] == place:
                for col in range(len(ru_fields1)):

                    ws.col(col).width = 256 * 32
                    ws.write(row_num,col,ru_fields1[col],column_style)

                row_num+=1

                for col in range(len(fields1)):
                    ws.write(row_num, col, info_table[i][fields1[col]], main_style)
                row_num+=1

                for col in range(len(ru_fields2)):
                    ws.write(row_num, col, ru_fields2[col], column_style)
                row_num+=1
                for row in stats_table[i]:
                    print('im here')
                    for col in range(len(fields2)):
                        if fields2[col]=='date_set' or fields2[col]=='date_changed':
                            print(row[fields2[col]].replace(tzinfo=None))
                            row[fields2[col]] = row[fields2[col]].replace(tzinfo=None)
                            ws.write(row_num, col, row[fields2[col]], date_style)
                        else:
                            ws.write(row_num,col,row[fields2[col]], main_style)
                    row_num += 1


    wb.save(return_obj)
    return return_obj

def export_toner_withdraw(request,obj,date_min = False,date_max=False):
    if not request.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    return_obj = HttpResponse(content_type='application/vnd.ms-excel')
    top_row = 1
    bottom_row = 3
    left_column = 0
    right_column = 7
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Report')
    row_num = 0
    column_style = xlwt.XFStyle()
    column_style.font.bold = True
    header_style = xlwt.easyxf("pattern: pattern solid, fore_color yellow; font: height 600, name Times New Roman"
                               ", color red; align: horiz center;")
    main_style = xlwt.XFStyle()

    places = set(dic['place__name'] for dic in obj['q'])  # unique places
    places = list(places)
    places.sort()
    print(places)

    fields = obj['fields']
    eng_fields = obj['eng_fields']
    fields.remove('ID')
    content = obj['q']
    print(content)
    for col in range(len(fields)):
        if col ==0 or 3 <= col <=4:
            ws.col(col).width = 256 * 20

        else:
            ws.col(col).width = 256 * 32
        ws.write(row_num,col,fields[col],column_style)
    # write in cell starts and end dates of the report
    ws.write(row_num, len(fields) + 1, "Начало периода", column_style)
    ws.write(row_num, len(fields) + 2, "Конец периода", column_style)

    if date_min:
        ws.write(1, len(fields) + 1, date_min, column_style)
        ws.col(len(fields) + 1).width = 256 * 17
    if date_max:
        ws.write(1, len(fields) + 2, date_max, column_style)
        ws.col(len(fields) + 2).width = 256 * 17

    for place in places:
        ws.write_merge(top_row + row_num, bottom_row + row_num, left_column, right_column, place, style=header_style)
        row_num = bottom_row + row_num
        for row in content:

            if row['place__name'] == place:
                row_num += 1
                for col in range(len(eng_fields)):
                    ws.write(row_num, col, row[eng_fields[col]], main_style)

    wb.save(return_obj)

    return return_obj

def obmen(request):
    if not request.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in ObmenFolders._meta.fields]

    folders = ObmenFolders.objects.all().order_by('-pk')
    context = {}
    context['filter'] = folders

    context['fields'] = fields
    paginated_set = Paginator(folders, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_set.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, 'obmen.html', context=context)

def obmen_update(response, pk):
    # update record from GiveDrum
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in ObmenFolders._meta.fields]
    class UpdateParams(UpdateView):
        template_name = 'update.html'
        model = ObmenFolders
        context_object_name = 'params'
        form_class = ObmenForms

        success_url = f"/obmen"

        extra_context = {'fields':fields}

        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            self.obj = queryset.get()

            return self.obj
        def get_success_url(self):
            return reverse('obmen')

    return UpdateParams.as_view()(response)

def folders_api(request):
    data = []
    for folder in ObmenFolders.objects.all():
        temp_data = {}
        temp_data.update(model_to_dict(folder))
        data.append(temp_data)

    import json
    response = json.dumps(data, ensure_ascii=False).encode('utf8')
    print(response)
    return HttpResponse(response)


