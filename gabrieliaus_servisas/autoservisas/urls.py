from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("carmodels/", views.carmodels, name="carmodels"),
    path("partservices/", views.partservices, name="partservices"),
    path("orderlines", views.orderlines, name="orderlines"),
    path('cardetail/<int:pk>/', views.car_detail, name='car_detail'),
    path('partservice/<int:pk>/', views.PartServiceDetailView.as_view(), name="partservice_detail"),
    path("masinos/mano/", views.CarUserListView.as_view(), name="cars_user"),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    path('create_partservice/<int:car_id>/', views.create_partservice_for_car, name='create_partservice'),
    path('user_part_service_detail/<int:car_id>/', views.user_part_service_detail, name='user_part_service_detail'),
    path('user_part_service_detail/<int:pk>/update/', views.CarPartServiceUpdateView.as_view(), name='carpartservice_update'),
    path('user_part_service_detail/<int:pk>/delete/', views.CarPartServiceDeleteView.as_view(), name='carpartservice_delete'),
]