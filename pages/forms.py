from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import GiveCartridge, RequestPrinters, GiveDrum,ObmenFolders
from django.contrib.auth.models import User
from admin_dashboard.models import DB_DCT
import django_filters
class GiveCartridgeForm(forms.ModelForm):

    printermodel = forms.ModelChoiceField(queryset=DB_DCT['printermodel'].objects.all(),
                                          label='Модель принтера',
                                          widget=forms.Select(attrs={'class': 'selectpicker','data-live-search':'true',
                                                              'data-size':'4', 'data-dropup-auto':'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                          empty_label='Выберете модель принтера')
    toner = forms.ModelChoiceField(queryset=DB_DCT['toner'].objects.all(), label='Модель картриджа'
                                   ,widget=forms.Select(attrs={'class': 'selectpicker','data-live-search':'true',
                                                              'data-size':'4', 'data-dropup-auto':'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                   empty_label='Выберете модель картриджа')
    place = forms.ModelChoiceField(queryset=DB_DCT['places'].objects.all(), label='Площадка' ,
                                   widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                              'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                   empty_label='Выберете площадку')
    department = forms.ModelChoiceField(queryset=DB_DCT['department'].objects.all(), label='Отдел',
                                   widget=forms.Select(attrs={'class': 'selectpicker','data-live-search':'true',
                                                              'data-size':'4', 'data-dropup-auto':'false',
                                                     'data-style':'btn btn-outline-primary'})
                                        ,empty_label='Выберете Отдел')
    amount = forms.ChoiceField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6)),label = 'Количество',
                               widget=forms.Select(attrs={'class': 'selectpicker',
                                                          'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'})
                               )
    comment = forms.CharField(max_length=200, required=False, label='Комментарий')
    # issued_by = forms.
    def __init__(self, *args, **kwargs):
        super(GiveCartridgeForm, self).__init__(*args, **kwargs)
        self.fields['issued_by'].disabled = True


    class Meta:
        model = GiveCartridge
        fields = '__all__'


class GiveDrumForm(forms.ModelForm):
    printermodel = forms.ModelChoiceField(queryset=DB_DCT['printermodel'].objects.all(),
                                          label='Модель принтера',
                                          widget=forms.Select(
                                              attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                     'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                          empty_label='Выберете модель принтера')
    drum = forms.ModelChoiceField(queryset=DB_DCT['drum'].objects.all(), label='Модель драма'
                                   , widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                   empty_label='Выберете модель драма')
    place = forms.ModelChoiceField(queryset=DB_DCT['places'].objects.all(), label='Площадка',
                                   widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                              'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'}),
                                   empty_label='Выберете площадку')
    department = forms.ModelChoiceField(queryset=DB_DCT['department'].objects.all(), label='Отдел',
                                        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                   'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style':'btn btn-outline-primary'})
                                        , empty_label='Выберете Отдел')

    def __init__(self, *args, **kwargs):
        super(GiveDrumForm, self).__init__(*args, **kwargs)
        self.fields['issued_by'].disabled = True


    class Meta:
        model = GiveDrum
        fields = '__all__'





class CartridgeFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
            attrs={'type':'date','class':'btn btn-outline-primary'}
        ),label='Период')
    printermodel = django_filters.ModelChoiceFilter(queryset=DB_DCT['printermodel'].objects.all(),
                                          label='Модель принтера',
                                          widget=forms.Select(
                                              attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                     'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style': 'btn btn-outline-primary'}),
                                          empty_label='Выберете модель принтера')
    toner = django_filters.ModelChoiceFilter(queryset=DB_DCT['toner'].objects.all(), label='Модель картриджа'
                                   , widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                'data-size': '4', 'data-dropup-auto': 'false',
                                                                'data-style': 'btn btn-outline-primary'}),
                                   empty_label='Выберете модель картриджа')
    place = django_filters.ModelChoiceFilter(queryset=DB_DCT['places'].objects.all(), label='Площадка',
                                   widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                              'data-size': '4', 'data-dropup-auto': 'false',
                                                              'data-style': 'btn btn-outline-primary'}),
                                   empty_label='Выберете площадку')
    department = django_filters.ModelChoiceFilter(queryset=DB_DCT['department'].objects.all(), label='Отдел',
                                        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                   'data-size': '4', 'data-dropup-auto': 'false',
                                                                   'data-style': 'btn btn-outline-primary'}),
                                                  empty_label='Выберете отдел')
    issued_by = django_filters.ModelChoiceFilter(queryset=User.objects.all(),label='Выдано(кем)',
                                        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                   'data-size': '4', 'data-dropup-auto': 'false',
                                                                   'data-style': 'btn btn-outline-primary'}),
                                                 empty_label='Выберете выдавшего')
    class Meta:
        model = GiveCartridge

        exclude = ('amount','comment')


class RequestFilterTest(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
            attrs={'type':'date','class':'btn btn-outline-primary'}
        ),label='Период')
    printer = django_filters.ModelChoiceFilter(queryset=DB_DCT['printers'].objects.all(),
                                          label='IP',
                                          widget=forms.Select(
                                              attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                     'data-size': '4', 'data-dropup-auto': 'false',
                                                     'data-style': 'btn btn-outline-primary'}),
                                          empty_label='Выберете модель принтера')

    class Meta:
        model = GiveCartridge

        fields = ['date','printer']

class DrumFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
            attrs={'type':'date','class':'btn btn-outline-primary'}
        ),label='Период')


    printermodel = django_filters.ModelChoiceFilter(queryset=DB_DCT['printermodel'].objects.all(),
                                                    label='Модель принтера',
                                                    widget=forms.Select(
                                                        attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                               'data-size': '4', 'data-dropup-auto': 'false',
                                                               'data-style': 'btn btn-outline-primary'}),
                                                    empty_label='Выберете модель принтера')
    drum = django_filters.ModelChoiceFilter(queryset=DB_DCT['drum'].objects.all(), label='Модель картриджа'
                                             , widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': 'true',
                   'data-size': '4', 'data-dropup-auto': 'false',
                   'data-style': 'btn btn-outline-primary'}),
                                             empty_label='Выберете модель картриджа')
    place = django_filters.ModelChoiceFilter(queryset=DB_DCT['places'].objects.all(), label='Площадка',
                                             widget=forms.Select(
                                                 attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                        'data-style': 'btn btn-outline-primary'}),
                                             empty_label='Выберете площадку')
    department = django_filters.ModelChoiceFilter(queryset=DB_DCT['department'].objects.all(), label='Отдел',
                                                  widget=forms.Select(
                                                      attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                             'data-size': '4', 'data-dropup-auto': 'false',
                                                             'data-style': 'btn btn-outline-primary'}),
                                                  empty_label='Выберете отдел')
    issued_by = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Выдано(кем)',
                                                 widget=forms.Select(
                                                     attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                            'data-size': '4', 'data-dropup-auto': 'false',
                                                            'data-style': 'btn btn-outline-primary'}),
                                                 empty_label='Выберете выдавшего')
    class Meta:
        model = GiveDrum

        exclude = ('comment',)

class RequestFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'type': 'date','class':'btn btn-outline-primary'}
    ))
    printer__printermodel = django_filters.ModelChoiceFilter(queryset=DB_DCT['printermodel'].objects.all(),
                                                    label='Модель принтера',
                                                    widget=forms.Select(
                                                        attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                               'data-size': '4', 'data-dropup-auto': 'false',
                                                               'data-style': 'btn btn-outline-primary'}),
                                                    empty_label='Выберете модель принтера')
    printer__toner = django_filters.ModelChoiceFilter(queryset=DB_DCT['toner'].objects.all(), label='Модель картриджа'
                                             , widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': 'true',
                   'data-size': '4', 'data-dropup-auto': 'false',
                   'data-style': 'btn btn-outline-primary'}),
                                             empty_label='Выберете модель картриджа')
    printer__place = django_filters.ModelChoiceFilter(queryset=DB_DCT['places'].objects.all(), label='Площадка',
                                             widget=forms.Select(
                                                 attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                        'data-style': 'btn btn-outline-primary'}),
                                             empty_label='Выберете площадку')



    class Meta:

        model = RequestPrinters
        # fields = '__all__'
        fields = ('date','printer__printermodel','printer__place','printer__toner',)


class TonerUtilsFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'type': 'date','class':'btn btn-outline-primary'}
    ))
    printer__printermodel = django_filters.ModelChoiceFilter(queryset=DB_DCT['printermodel'].objects.all(),
                                                             label='Модель принтера',
                                                             widget=forms.Select(
                                                                 attrs={'class': 'selectpicker',
                                                                        'data-live-search': 'true',
                                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                                        'data-style': 'btn btn-outline-primary'}),
                                                             empty_label='Выберете модель принтера')
    printer__toner = django_filters.ModelChoiceFilter(queryset=DB_DCT['toner'].objects.all(), label='Модель картриджа'
                                                      , widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': 'true',
                   'data-size': '4', 'data-dropup-auto': 'false',
                   'data-style': 'btn btn-outline-primary'}),
                                                      empty_label='Выберете модель картриджа')
    printer__place = django_filters.ModelChoiceFilter(queryset=DB_DCT['places'].objects.all(), label='Площадка',
                                                      widget=forms.Select(
                                                          attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                 'data-size': '4', 'data-dropup-auto': 'false',
                                                                 'data-style': 'btn btn-outline-primary'}),
                                                      empty_label='Выберете площадку')
    printer = django_filters.ModelChoiceFilter(queryset=DB_DCT['printers'].objects.all(), label='IP',
                                                      widget=forms.Select(
                                                          attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                                 'data-size': '4', 'data-dropup-auto': 'false',
                                                                 'data-style': 'btn btn-outline-primary'}),
                                                      empty_label='Выберете IP')
    class Meta:
        model = RequestPrinters
        fields = ('date','printer__place','printer__toner','printer__printermodel','printer')


class ObmenForms(forms.ModelForm):
    name = forms.CharField(max_length=200)
    description = forms.Textarea()
    visible = forms.CheckboxInput()
    class Meta:

        model = ObmenFolders
        fields = '__all__'
