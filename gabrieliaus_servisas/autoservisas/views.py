from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models, forms
from django.utils.translation import gettext_lazy as _

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
        messages.success(self.request, _('Atsiliepimas pridėtas sėkmingai.'))
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('partservice_detail', kwargs={'pk': self.object.pk})
    
class CarCreateView(LoginRequiredMixin, CreateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'autoservisas/car_form.html'
    success_url = reverse_lazy('cars_user')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Mašina pridėta sėkmingai.')
        return super().form_valid(form)

class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'autoservisas/car_form.html'
    success_url = reverse_lazy('cars_user')

    def form_valid(self, form):
        messages.success(self.request, 'Mašina pakeista sėkmingai.')
        return super().form_valid(form)

class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Car
    template_name = 'autoservisas/car_confirm_delete.html'
    success_url = reverse_lazy('cars_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context['car'] = car
        return context

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, 'Mašina ištrinta sėkmingai.')
        return reverse('cars_user')

def create_partservice_for_car(request, car_id):
    car = get_object_or_404(models.Car, pk=car_id, owner=request.user)
    if request.method == 'POST':
        form = forms.PartServiceForm(request.POST)
        if form.is_valid():
            part_service = form.cleaned_data['existing_part_service']
            problem = form.cleaned_data['problem']
            car_part_service = models.CarPartService(
                car=car,
                part_service=part_service,
                problem=problem
            )
            car_part_service.save()
            
            return redirect('cars_user')
    else:
        form = forms.PartServiceForm()
    
    existing_partservices = models.PartService.objects.all()

    context = {
        'car': car,
        'form': form,
        'existing_partservices': existing_partservices,
    }
    return render(request, 'autoservisas/create_partservice.html', context)


def user_part_service_detail(request, car_id):
    car = get_object_or_404(models.Car, pk=car_id, owner=request.user)
    partservices = models.CarPartService.objects.filter(car=car).select_related('part_service')
    
    context = {
        'car': car,
        'partservices': partservices,
    }
    return render(request, 'autoservisas/user_part_service_detail.html', context)


class CarPartServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CarPartService
    form_class = forms.PartServiceForm
    template_name = 'autoservisas/create_partservice.html'

    def get_success_url(self):
        return reverse('user_part_service_detail', kwargs={'car_id': self.object.car.id})

    def form_valid(self, form):
        messages.success(self.request, 'Paslauga atnaujinta sėkmingai.')
        return super().form_valid(form)

class CarPartServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = models.CarPartService
    template_name = 'autoservisas/carpartservice_confirm_delete.html'
    success_url = reverse_lazy('user_part_service_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carpartservice = self.get_object()
        context['carpartservice'] = carpartservice
        return context

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Paslauga ištrinta sėkmingai.')
        return reverse('user_part_service_detail', kwargs={'car_id': self.object.car.id})
