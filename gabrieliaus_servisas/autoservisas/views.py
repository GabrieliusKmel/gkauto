from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from . import models, forms

class CarUserListView(LoginRequiredMixin, generic.ListView):
    model = models.Car
    template_name = "autoservisas/car_user_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

def index(request):
    context = {
        "num_carmodels": models.CarModel.objects.count(),
        "num_cars": models.Car.objects.count(),
        "num_service_orders": models.ServiceOrder.objects.count(),
        "num_partservice": models.PartService.objects.count(),
        "num_orderlines": models.OrderLine.objects.count(),
        "car_model_brands": models.CarModel.objects.values_list("brand", flat=True).distinct(),
        "partandservice": models.PartService.objects.values_list("name", "price").distinct()
    }
    return render(request, "autoservisas/index.html", context)

def carmodels(request):
    query = request.GET.get('query', '')
    carmodels_query = models.CarModel.objects.all()
    if query:
        carmodels_query = carmodels_query.filter(
            Q(brand__icontains=query) | Q(model__icontains=query)
        )
    carmodels_pages = Paginator(carmodels_query, 3)
    current_page = request.GET.get('page') or 1
    current_page_obj = carmodels_pages.get_page(current_page)
    context = {
        "carmodels": current_page_obj,
    }
    return render(request, "autoservisas/carmodels.html", context)

def partservices(request):
    return render(
        request,
        "autoservisas/partservices.html",
        {"partservices": models.PartService.objects.all()}
    )

def orderlines(request):
    orderlines = models.OrderLine.objects.all().order_by('order__date')
    return render(
        request,
        "autoservisas/orderlines.html",
        {"orderlines": orderlines}
    )

def car_detail(request, pk):
    return render(
        request,
        "autoservisas/car_detail.html",
        {"car_detail": get_object_or_404(models.Car, pk=pk)}
    )

def orderlines(request):
    query = request.GET.get('uzsakymai', '')
    orderlines_query = models.OrderLine.objects.all()
    if query:
        orderlines = orderlines_query.filter(
            Q(order__car__customer__icontains=query) |
            Q(part_service__name__icontains=query) |
            Q(order__status__icontains=query) 
        ).order_by('order__date')
    else:
        orderlines = orderlines_query.order_by('order__date')
    orderlines_pages = Paginator(orderlines, 2)
    current_page = request.GET.get('page') or 1
    current_page_obj = orderlines_pages.get_page(current_page)
    context = {
        "orderlines": current_page_obj,
        "all_orderlines": orderlines, 
    }
    return render(request, "autoservisas/orderlines.html", context)


class PartServiceDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.PartService
    template_name = 'autoservisas/partservice_detail.html'
    form_class = forms.PartServiceReviewForm

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['partservice'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial

    def post(self, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form) -> HttpResponse:
        form.instance.partservice = self.object
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, 'Atsiliepimas pridėtas sėkmingai.')
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('partservice_detail', kwargs={'pk': self.object.pk})