def dashboard_main(response):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")

    return render(response, 'dashboard.html')

def dashboard_type(response, type):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    return render(response, 'dashboard.html', {'type':type})





from django.views.generic.list import ListView


class DisplayParams(ListView):
    model = DB_DCT['printermodel']
    paginate_by = 10
    context_object_name = 'params'
    template_name = 'dashboard.html'




def add_new(response,type,action):
    if not response.user.is_authenticated:
        return redirect(f"/admin_dashboard/login")
    if response.method == "POST":
        form = FORM_DCT[type](response.POST)
        if form.is_valid():

            n = form.cleaned_data['name']
            t = DB_DCT[type]()
            t.name = n
            t.save()

            return redirect(f"/admin_dashboard/?type={type}")
    else:
        form = FORM_DCT[type]()
        return render(response, 'dashboard.html', {'form':form, 'type':type,'action':action})