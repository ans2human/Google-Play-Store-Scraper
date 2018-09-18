from django.urls import path
from . import views
from gpscraper.views import HomeView, AppSearchView, AppDetailView, Results

app_name = "gpscraper"


urlpatterns = [

    path('', views.HomeView, name='home'),

    path('app/search/', AppSearchView.as_view(), name='app_search'),

    path('app/results/', views.Results, name='results'),

    path('app/detail/<uid>/', AppDetailView.as_view(), name='app_detail'),

]

