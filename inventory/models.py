from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
CATEGORY = (
        ('GINGER ME', 'Ginger Me'),
        ('COCOA MY KOKO', 'Cocoa My Koko'),
        ('GREEN WITH ENVY', 'Green With Envy'),
        ('INIGHE', 'Inighe'),
        ('LA VIDA LOCA', 'La Vida Loca'),
        ('NUTTY BY NATURE', 'Nutty By Nature'),
        ('TRIPLE THREAT', 'Triple THreat'),
    )


class Category(models.Model):
    name = models.CharField(choices=CATEGORY, blank=False, max_length=20)
    price = models.CharField(default=500, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


ORDER_STATUS = (
            ('DELIVERED', 'delivered'),
            ('UNDELIVERED', 'undelivered'),
            ('OTHERS', 'others'),
            ('READY', 'ready'),
            ('NOT-READY', 'not-ready'),
    )


class OrderStatus(models.Model):
    name = models.CharField(choices=ORDER_STATUS, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Order Status"


class CustomerOrders(models.Model):
    user = models.ForeignKey(User)
    cust_name = models.CharField(unique=True, max_length=200, blank=False)
    address = models.TextField(blank=False)
    product_quant = models.CharField(max_length=300, blank=False, default = "")
    product_value = models.IntegerField(blank=False, default="")
    date_added = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    phone_no = models.CharField(max_length=100, blank=False)
    state = models.CharField(blank=False, max_length=100, default="")
    category = models.ForeignKey(Category)
    coms_exec = models.CharField(default="", max_length=50)
    amount_paid = models.IntegerField(default=0)
    date_paid = models.DateTimeField(default=timezone.now)
    d_person = models.CharField(max_length=100, default="")
    order_status = models.CharField(max_length=50, default="Not Yet Specified")
    comment = models.TextField(blank=True, default="")
    status = models.CharField(default="", max_length=50)

    def __str__(self):
        return "%s %s" % (self.cust_name, self.coms_exec)

    class Meta:
        verbose_name_plural = "customer orders"


class ComsReps(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.user.username


class StateCountry(models.Model):
    name = models.CharField(max_length=100, default="", blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "states/countries"
        ordering = ('name',)


class LagosLocations(models.Model):
    name = models.CharField(max_length=100, default="", blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "lagos locations"


class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100, default="", blank=False)

    def __str__(self):
        return self.name


class DeliveryPersonCharges(models.Model):
    d_person = models.CharField(max_length=100, default="")
    capital = models.IntegerField(default=0, blank=True)
    commission = models.IntegerField(default=0, blank=True)
    incentive = models.IntegerField(default=0, blank=True)
    expenses = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    total = models.IntegerField(default=0, blank=True)
    next_capital = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.d_person


class DeliveryPersonCash(models.Model):
    d_person = models.CharField(max_length=100, default="")
    count = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    total = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.d_person


STATUS = (
            ('URGENT', 'urgent'),
            ('NOT URGENT', 'not'),
    )


class Status(models.Model):
    name = models.CharField(choices=STATUS, max_length=100, default="", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"


class Stock(models.Model):
    name = models.CharField(max_length=100, blank=False)
    ginger_me = models.IntegerField(default=0, blank=False)
    ginger_me_value = models.IntegerField(default=0, blank=False)
    cocoa_my_koko = models.IntegerField(default=0, blank=False)
    cocoa_my_koko_value = models.IntegerField(default=0, blank=False)
    green_with_envy = models.IntegerField(default=0, blank=False)
    green_with_envy_value = models.IntegerField(default=0, blank=False)
    inighe = models.IntegerField(default=0, blank=False)
    inighe_value = models.IntegerField(default=0, blank=False)
    la_vida_loca = models.IntegerField(default=0, blank=False)
    la_vida_loca_value = models.IntegerField(default=0, blank=False)
    nutty_by_nature = models.IntegerField(default=0, blank=False)
    nutty_by_nature_value = models.IntegerField(default=0, blank=False)
    triple_threat = models.IntegerField(default=0, blank=False)
    triple_threat_value = models.IntegerField(default=0, blank=False)
    add_stock = models.IntegerField(default=0, blank=False)
    substract_stock = models.IntegerField(default=0, blank=False)
    current_stock = models.IntegerField(default=0, blank=False)
    date_updated = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0, blank=False)
    remarks = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Stocks"


class StockValues(models.Model):
    name = models.CharField(max_length=100, blank=False)
    ginger_me_value = models.IntegerField(default=0, blank=True)
    cocoa_my_koko_value = models.IntegerField(default=0, blank=True)
    green_with_envy_value = models.IntegerField(default=0, blank=True)
    inighe_value = models.IntegerField(default=0, blank=True)
    la_vida_loca_value = models.IntegerField(default=0, blank=True)
    nutty_by_nature_value = models.IntegerField(default=0, blank=True)
    triple_threat_value = models.IntegerField(default=0, blank=True)
    total_value = models.IntegerField(default=0, blank=True)
    remarks_value = models.CharField(max_length=100, blank=True, default="")
    date_added = models.CharField(max_length=100, blank=True, default="")
    stock_added = models.CharField(max_length=100, blank=True, default="")
    stock_removed = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Stock Values"