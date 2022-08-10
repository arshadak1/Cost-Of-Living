from django.contrib import admin
from django.urls import path, include
from . import views
from .views import DataDetailView, DataListView, DataCreateView, DataUpdateView, DataDeleteView

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/profile', views.profile, name="profile"),
    path('dashboard/graphs', views.graphs, name="graphs"),
    path('review', views.review, name="review"),
    # here we create a seperate Model(Database table) and we create class in views.py
    path('dashboard/datas', DataListView.as_view(), name="data"),
    path('dashboard/data/<int:pk>/', DataDetailView.as_view(), name="data-detail"), # deprecated
    path('dashboard/data-create', DataCreateView.as_view(), name="data-create"),
    path('dashboard/data-update/<int:pk>/', DataUpdateView.as_view(), name="data-update"),
    path('dashboard/data-delete/<int:pk>/', DataDeleteView.as_view(), name="data-delete"),
    

]
