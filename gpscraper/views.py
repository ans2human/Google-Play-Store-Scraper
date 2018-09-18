import requests
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import View
from gpscraper.models import AppData, AppSearchIndex
from gpscraper.forms import SearchForm
from gpscraper.helper import PlayStoreHelper
from django.db.models import Q


    

def HomeView(request):
    ayo = "Google Play Store Scraper"
    context = { 'ayo':ayo}
    template_path = 'gpscraper/home.html'
    return render(request, template_path, context)



class AppSearchView(FormView):

    template_name = 'gpscraper/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        query = form.cleaned_data.get('query', None)
        print(query)
        result = PlayStoreHelper.search(query)
        print(result)
        context = {'form': self.form_class, 'result': result}
        return render(self.request, self.template_name, context)


class AppDetailView(View):

    template_name = 'gpscraper/detail.html'

    def get(self, request, uid):
        app_data = PlayStoreHelper.get_app_details(uid)
        return render(self.request, self.template_name, app_data)



def Results(request):

    result = AppData.objects.all()
    query = request.GET.get("q")
    if query:
        result = result.filter(
            Q(name__icontains=query)|
            Q(uid__icontains=query)|
            Q(dev_name__icontains=query)


        ).distinct()
    return render(request, 'gpscraper/resultlist.html', {'result': result,})
