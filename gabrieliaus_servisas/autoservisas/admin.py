from django.contrib import admin
from . import models

class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0

class ServiceOrderInline(admin.TabularInline):
    model = models.ServiceOrder
    extra = 0

class CarAdmin(admin.ModelAdmin):
    list_display = ("customer", "car_model", "plate", "vin", "color", "owner")
    list_filter = ("car_model__brand", "color")
    list_display_links = ("customer",)
    search_fields = ("customer", "plate", "vin")
    inlines = [ServiceOrderInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year")
    list_filter = ("year",)
    list_display_links = ("brand",)
    search_fields = ("brand", "model")

class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("car", "date", "get_status_display")
    list_filter = ("date", "status")
    list_display_links = ("car",)
    search_fields = ("car__customer", "car__plate", "car__vin")
    readonly_fields = ("id",)
    inlines = [OrderLineInline]

class PartServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    list_display_links = ("name",)
    search_fields = ("name", "price")

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("order", "order_car_customer", "part_service", "quantity", "price")
    list_filter = ("order__status", "order__date")
    list_display_links = ("order",)
    search_fields = ("order__car__customer", "part_service__name")

    def order_car_customer(self, obj):
        return obj.order.car.customer
    order_car_customer.short_description = "Customer"
    order_car_customer.admin_order_field = "order__car__customer"

@admin.register(models.PartServiceReview)
class PartServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('partservice', 'reviewer', 'created_at')
    list_display_links = ('created_at', )

admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.PartService, PartServiceAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)