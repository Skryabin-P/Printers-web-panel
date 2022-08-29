from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView,CreateView, UpdateView
from .forms import FORM_DCT
from .models import DB_DCT
def sign_up(response):
    if response.method == 'POST':
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            redirect("/")
    else:
        form = UserCreationForm()
    return render(response,"sign_up.html", {'form':form})


def dashboard_main(response):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")

    return render(response, 'dashboard.html')

def dashboard_type(response, type):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in DB_DCT[type]._meta.fields]
    print(fields)
    # my_list = DB_DCT[type].objects.all()
    # return render(response, 'dashboard.html', {'type':type, 'params':my_list})

    return ListView.as_view(model=DB_DCT[type],paginate_by=10, context_object_name='params', extra_context={'type':type, 'fields':fields}, template_name='dashboard.html')(response)








# class DisplayParams(ListView):
#     model = DB_DCT['printermodel']
#     paginate_by = 10
#     context_object_name = 'params'
#     extra_context = type
#     template_name = 'dashboard.html'




def add_new(response,type,action):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    class CreateMyView(CreateView):
        model = DB_DCT[type]
        template_name = 'dashboard.html'
        # form = FORM_DCT[type]
        # context_object_name = 'form'\
        form_class = FORM_DCT[type]
        extra_context = {'action':action}
        # fields = [f.name for f in DB_DCT[type]._meta.get_fields()]

        success_url = f"/admin_dashboard/{type}"



    return CreateMyView.as_view()(response)

    # if response.method == "POST":
    #     form = FORM_DCT[type](response.POST)
    #     print('Im here2')
    #     for field in form:
    #         print("Field Error:", field.name,  field.errors)
    #     if form.is_valid():
    #         print('Im here')
    #         n = form.cleaned_data['name']
    #         t = DB_DCT[type]()
    #         t.name = n
    #         t.save()
    #
    #     return redirect(f"/admin_dashboard/{type}")
    # else:
    #     print('Im here 3')
    #     form = FORM_DCT[type]()
    #     return render(response, 'dashboard.html', {'form':form, 'type':type,'action':action})

def update_data(response, type, pk):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.name for f in DB_DCT[type]._meta.fields]
    class UpdateParams(UpdateView):
        template_name = 'update1.html'
        model = DB_DCT[type]
        context_object_name = 'params'
        form_class = FORM_DCT[type]

        # form = FORM_DCT[type]
        extra_context = {'fields': fields}

        # fields = '__all__'
        success_url = f"/admin_dashboard/{type}"

        # initial = self.obj.__dict__
        # def get(self, request, *args, **kwargs):
        #     form = self.form_class(initial=self.initial)
        #     return render(request, self.template_name, {'form': form})

        def get_initial(self):
            fields_form = [f.name for f in DB_DCT[type]._meta.fields]
            base_initial = {}
            values = self.obj.get_string_fields()

            i = 0
            for field in fields_form:
                base_initial[field] = values[i]
                i+=1
            print(base_initial)
            return base_initial

        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)

            self.obj = queryset.get()

            return self.obj
        def get_success_url(self):
            return reverse('dashboard_type',kwargs={'type':type})
    return UpdateParams.as_view()(response)
def delete_data(response,type,pk):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.name for f in DB_DCT[type]._meta.fields]
    class DeleteParams(DeleteView):
        template_name = 'delete1.html'
        model = DB_DCT[type]
        context_object_name = 'params'
        extra_context = {'fields':fields,'type':type}
        def get_object(self, queryset=None):
            if queryset is None:
                queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
            return obj
        def get_success_url(self):
            return reverse('dashboard_type',kwargs={'type':type})
        # model = DB_DCT[type]
        # def get_object(self, queryset=None):
        #     id = self.kwargs.get("id")
        #     return get_object_or_404(DB_DCT[type],id=id)
        # def get_success_url(self):
        #     return reverse(type)

    return DeleteParams.as_view()(response)

    # return DeleteView.as_view(model=DB_DCT[type], context_object_name='params', template_name='delete1.html')(response)

# class Dashboard(TemplateView):
#     template_name = 'dashboard.html'
#     # def get(self,response):
#     #     if response.method == "GET":
#     #         return render(response, 'dashboard.html')
#     def select_option(self,response):
#         self.result = response.GET
#         if 'type' in self.result.keys():
#
#             return render(response, 'dashboard.html', {'type': self.result['type']})
#
#     def select_action(self,response):
#         if 'action' in self.result.keys():
#             if self.result['action'] == 'add':
#                 return self.add_new(self.result['type'], self.result['action'],response)
#
#     def add_new(self,type,action,response):
#         if response.method == "POST":
#             form = AddPrinterModel(response.POST)
#             if form.is_valid():
#                 n = form.cleaned_data['name']
#                 t = PrinterModelList()
#                 t.name = n
#                 t.save()
#
#                 return redirect(f"/admin_dashboard/?type={type}")
#         else:
#             print('Im here 6')
#             form = AddPrinterModel()
#             return render(response, 'dashboard.html', {'form': form, 'type': type, 'action': action})




