from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CarModel(models.Model):
    brand = models.CharField(_("brand"), max_length=50, db_index=True)
    model = models.CharField(_("model"), max_length=50, db_index=True)
    year = models.IntegerField(_("year"), db_index=True)

    class Meta:
        verbose_name = _("carmodel")
        verbose_name_plural = _("carmodels")
        ordering = ["brand", "model", "year"]

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})
    

class Car(models.Model):
    customer = models.CharField(_("customer"), max_length=50, db_index=True)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_("carmodel"),
        on_delete=models.CASCADE,
        related_name="cars",
        )
    plate = models.CharField(_("plate"), max_length=10)
    vin = models.CharField(_("vin"), max_length=17)
    color = models.CharField(_("color"), max_length=20)

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")
        ordering = ["customer"]

    def __str__(self):
        return f"{self.customer} {self.plate} {self.vin}"

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})

SERVICEORDER_STATUS = (
    (0, _("pending")),
    (1, _("in progress")),
    (2, _("completed")),
    (3, _("cancelled")),
)

class ServiceOrder(models.Model):
    car = models.ForeignKey(
        Car,
        verbose_name=_("car"),
        on_delete=models.CASCADE,
        related_name="orders",
        db_index=True,
    )
    date = models.DateField(_("date"), auto_now=False, auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=SERVICEORDER_STATUS, 
        default=0
    )

    class Meta:
        verbose_name = _("serviceorder")
        verbose_name_plural = _("serviceorders")
        ordering = ["car"]

    def __str__(self):
        return f"{self.car} {self.date} {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse("serviceorder_detail", kwargs={"pk": self.pk})

class PartService(models.Model):
    name = models.CharField(_("name"), max_length=50, db_index=True)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = _("partservice")
        verbose_name_plural = _("partservices")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} Kaina {self.price}"

    def get_absolute_url(self):
        return reverse("partservice_detail", kwargs={"pk": self.pk})    

class OrderLine(models.Model):
    order = models.ForeignKey(
        ServiceOrder,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name="lines",
        db_index=True,
        )
    part_service = models.ForeignKey(
        PartService,
        verbose_name=_("part service id"),
        on_delete=models.CASCADE,
        related_name="lines",
        )
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    
    class Meta:
        verbose_name = _("orderline")
        verbose_name_plural = _("orderlines")
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} {self.part_service} Kiekis {self.quantity} Papildomos išlaidos {self.price}"

    def get_absolute_url(self):
        return reverse("orderline_detail", kwargs={"pk": self.pk})



