from django import forms
from .models import DB_DCT



class AddPrinterModel(forms.ModelForm):
    class Meta:
        model = DB_DCT['printermodel']
        fields = '__all__'

class AddTonerModel(forms.ModelForm):
    class Meta:
        model = DB_DCT['toner']
        fields = '__all__'

class AddPlaces(forms.ModelForm):
    class Meta:
        model = DB_DCT['places']
        fields = '__all__'

class AddDepartment(forms.ModelForm):
    class Meta:
        model = DB_DCT['department']
        fields = '__all__'

class AddDrum(forms.ModelForm):
    class Meta:
        model = DB_DCT['drum']
        fields = '__all__'

class AddNewPrinter(forms.ModelForm):
    printermodel = forms.ModelChoiceField(queryset=DB_DCT['printermodel'].objects.all(),
                                                             widget=forms.Select(
                                                                 attrs={'class': 'selectpicker',
                                                                        'data-live-search': 'true',
                                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                                        'data-style': 'btn btn-outline-primary'}),
                                                             empty_label='Выберете модель принтера')
    toner = forms.ModelChoiceField(queryset=DB_DCT['toner'].objects.all(),
                                                             widget=forms.Select(
                                                                 attrs={'class': 'selectpicker',
                                                                        'data-live-search': 'true',
                                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                                        'data-style': 'btn btn-outline-primary'}),
                                                             empty_label='Выберете модель картриджа')
    place = forms.ModelChoiceField(queryset=DB_DCT['places'].objects.all(),
                                                             widget=forms.Select(
                                                                 attrs={'class': 'selectpicker',
                                                                        'data-live-search': 'true',
                                                                        'data-size': '4', 'data-dropup-auto': 'false',
                                                                        'data-style': 'btn btn-outline-primary'}),
                                                             empty_label='Выберете модель принтера')

    class Meta:

        model = DB_DCT['printers']


        fields = '__all__'




FORM_DCT = {'printermodel': AddPrinterModel,'toner':AddTonerModel, 'places':AddPlaces,
            'printers':AddNewPrinter, 'department':AddDepartment,'drum':AddDrum}
#name = forms.CharField(label="Type printer model name", max_length=200, required=True)
#name = forms.CharField(label="Type toner model name", max_length=200, required=True)
# name = forms.CharField(label="Type name of the Place", max_length=200, required=True)
# ip = forms.GenericIPAddressField(label="Type an IP adress", required=True, protocol='IPv4')
#     model = forms.ModelChoiceField(label="Choose printer model",queryset=DB_DCT['printermodel'].objects.all())
#     toner = forms.ModelChoiceField(label="Choose toner model",queryset=DB_DCT['toner'].objects.all())
#     place = forms.ModelChoiceField(label="Choose place where printer is placed",queryset=DB_DCT['places'].objects.all())
#     comment = forms.CharField(label = "Type your comment",max_length=200, required=False)