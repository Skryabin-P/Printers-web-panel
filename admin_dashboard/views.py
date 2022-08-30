from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView,CreateView, UpdateView
from .forms import FORM_DCT
from .models import DB_DCT
def sign_up(response):
    # sign up to admin dashboard, not django admin
    if response.method == 'POST':
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            redirect("/")
    else:
        form = UserCreationForm()
    return render(response,"sign_up.html", {'form':form})


def dashboard_main(response):
    # main menu of an admin dashboard
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")

    return render(response, 'dashboard.html')

def dashboard_type(response, type):
    # list of parameters to change
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.verbose_name for f in DB_DCT[type]._meta.fields]
    print(fields)

    return ListView.as_view(model=DB_DCT[type],paginate_by=10, context_object_name='params', extra_context={'type':type, 'fields':fields}, template_name='dashboard.html')(response)


def add_new(response,type,action):
    # Add new parameter like printer(ip,model etc), printer model, toner model,place etc
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    class CreateMyView(CreateView):
        model = DB_DCT[type]
        template_name = 'dashboard.html'
        form_class = FORM_DCT[type]
        extra_context = {'action':action}


        success_url = f"/admin_dashboard/{type}"



    return CreateMyView.as_view()(response)



def update_data(response, type, pk):
    # update dashboard parameters
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    fields = [f.name for f in DB_DCT[type]._meta.fields]
    class UpdateParams(UpdateView):
        template_name = 'update1.html'
        model = DB_DCT[type]
        context_object_name = 'params'
        form_class = FORM_DCT[type]


        extra_context = {'fields': fields}

        success_url = f"/admin_dashboard/{type}"


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
    # delete admin parameters
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

    return DeleteParams.as_view()(response)




