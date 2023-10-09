from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("carmodels/", views.carmodels, name="carmodels"),
    path("partservices/", views.partservices, name="partservices"),
    path("orderlines", views.orderlines, name="orderlines"),
    path('cardetail/<int:pk>/', views.car_detail, name='car_detail'),
    path('partservice/<int:pk>/', views.PartServiceDetailView.as_view(), name="partservice_detail"),
    path("masinos/mano/", views.CarUserListView.as_view(), name="cars_user")
]