from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.forms import CustomerOrderForm, ConfirmCustomerOrderForm, OrderStatusForm, StockForm, AddStockForm, RemoveStockForm, DeliveryPersonChargesForm, LagosCustomerOrderForm, DeliveryPersonCashForm, DeliveryPersonCash
from django.contrib import messages
from inventory.models import Category, ComsReps, CustomerOrders, StateCountry, OrderStatus, Stock, StockValues, DeliveryPersonCharges
from django.db.models import Q, F
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
# Create your views here.

today = datetime.now().date()
yesterday = today - timedelta(1)
last_week = today - timedelta(days=7)
last_month = today - timedelta(days=30)
last_year = today - timedelta(days=365)


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"

def myview(request):
    data = download_csv(CustomerOrderForm, request, Model.objects.all())

    return HttpResponse (data, content_type='text/csv')

@login_required
def home(request):
    categories = Category.objects.all()
    is_dperson = request.user.groups.filter(name='dperson').exists()
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    is_stock = request.user.groups.filter(name='stock').exists()
    is_comsexec = request.user.groups.filter(name='comsexec').exists()
    user_orders = CustomerOrders.objects.filter(user_id=request.user.id)
    user_processed_orders = CustomerOrders.objects.filter(coms_exec=request.user.username).exclude(amount_paid__exact=0)
    user_coms_today_product_value = CustomerOrders.objects.filter(date_added=today, coms_exec=request.user.username).aggregate(Sum('product_value'))
    user_coms_all_product_value = CustomerOrders.objects.filter(coms_exec=request.user.username).aggregate(Sum('product_value'))
    user_coms_all_amount_paid = CustomerOrders.objects.filter(coms_exec=request.user.username).aggregate(Sum('amount_paid'))
    user_coms_week_amount_paid = CustomerOrders.objects.filter(date__range=["2017-03-15", "2017-03-21"], coms_exec=request.user.username).aggregate(Sum('amount_paid'))
    coms_orders = CustomerOrders.objects.filter(coms_exec=request.user.username)
    coms_orders_today = CustomerOrders.objects.filter(coms_exec=request.user.username, date_added=today)
    coms_orders_yesterday = CustomerOrders.objects.filter(coms_exec=request.user.username, date_added=yesterday)
    coms_orders_last_week = CustomerOrders.objects.filter(coms_exec=request.user.username, date_added__gte=last_week)
    coms_orders_last_month = CustomerOrders.objects.filter(coms_exec=request.user.username, date_added__gte=last_month)
    coms_orders_last_year = CustomerOrders.objects.filter(coms_exec=request.user.username, date_added__gte=last_year)
    orders_slimtea_today = CustomerOrders.objects.filter(category_id=1, amount_paid__exact=0, date_added=today)
    orders_slimtea_yesterday = CustomerOrders.objects.filter(category_id=1, amount_paid__exact=0, date_added=yesterday)
    orders_slimtea_last_week = CustomerOrders.objects.filter(category_id=1, amount_paid__exact=0, date_added__gte=last_week)
    orders_slimtea_last_month = CustomerOrders.objects.filter(category_id=1, amount_paid__exact=0, date_added__gte=last_month)
    orders_slimtea_last_year = CustomerOrders.objects.filter(category_id=1, amount_paid__exact=0, date_added__gte=last_year)
    orders_waist_today = CustomerOrders.objects.filter(category_id=2, amount_paid__exact=0, date_added=today)
    orders_waist_yesterday = CustomerOrders.objects.filter(category_id=2, amount_paid__exact=0, date_added=yesterday)
    orders_waist_last_week = CustomerOrders.objects.filter(category_id=2, amount_paid__exact=0, date_added__gte=last_week)
    orders_waist_last_month = CustomerOrders.objects.filter(category_id=2, amount_paid__exact=0, date_added__gte=last_month)
    orders_waist_last_year = CustomerOrders.objects.filter(category_id=2, amount_paid__exact=0, date_added__gte=last_year)
    orders_mecran_today = CustomerOrders.objects.filter(category_id=3, amount_paid__exact=0, date_added=today)
    orders_mecran_yesterday = CustomerOrders.objects.filter(category_id=3, amount_paid__exact=0, date_added=yesterday)
    orders_mecran_last_week = CustomerOrders.objects.filter(category_id=3, amount_paid__exact=0, date_added__gte=last_week)
    orders_mecran_last_month = CustomerOrders.objects.filter(category_id=3, amount_paid__exact=0, date_added__gte=last_month)
    orders_mecran_last_year = CustomerOrders.objects.filter(category_id=3, amount_paid__exact=0, date_added__gte=last_year)
    orders_flattummy_today = CustomerOrders.objects.filter(category_id=4, amount_paid__exact=0, date_added=today)
    orders_flattummy_yesterday = CustomerOrders.objects.filter(category_id=4, amount_paid__exact=0, date_added=yesterday)
    orders_flattummy_last_week = CustomerOrders.objects.filter(category_id=4, amount_paid__exact=0, date_added__gte=last_week)
    orders_flattummy_last_month = CustomerOrders.objects.filter(category_id=4, amount_paid__exact=0, date_added__gte=last_month)
    orders_flattummy_last_year = CustomerOrders.objects.filter(category_id=4, amount_paid__exact=0, date_added__gte=last_year)

    orders_moolato_today = CustomerOrders.objects.filter(category_id=6, amount_paid__exact=0, date_added=today)
    orders_moolato_yesterday = CustomerOrders.objects.filter(category_id=6, amount_paid__exact=0, date_added=yesterday)
    orders_moolato_last_week = CustomerOrders.objects.filter(category_id=6, amount_paid__exact=0, date_added__gte=last_week)
    orders_moolato_last_month = CustomerOrders.objects.filter(category_id=6, amount_paid__exact=0, date_added__gte=last_month)
    orders_moolato_last_year = CustomerOrders.objects.filter(category_id=6, amount_paid__exact=0, date_added__gte=last_year)

    orders_hairnownow_today = CustomerOrders.objects.filter(category_id=5, amount_paid__exact=0, date_added=today)
    orders_hairnownow_yesterday = CustomerOrders.objects.filter(category_id=5, amount_paid__exact=0, date_added=yesterday)
    orders_hairnownow_last_week = CustomerOrders.objects.filter(category_id=5, amount_paid__exact=0, date_added__gte=last_week)
    orders_hairnownow_last_month = CustomerOrders.objects.filter(category_id=5, amount_paid__exact=0, date_added__gte=last_month)
    orders_hairnownow_last_year = CustomerOrders.objects.filter(category_id=5, amount_paid__exact=0, date_added__gte=last_year)

    orders_hairnymph_today = CustomerOrders.objects.filter(category_id=7, amount_paid__exact=0, date_added=today)
    orders_hairnymph_yesterday = CustomerOrders.objects.filter(category_id=7, amount_paid__exact=0, date_added=yesterday)
    orders_hairnymph_last_week = CustomerOrders.objects.filter(category_id=7, amount_paid__exact=0, date_added__gte=last_week)
    orders_hairnymph_last_month = CustomerOrders.objects.filter(category_id=7, amount_paid__exact=0, date_added__gte=last_month)
    orders_hairnymph_last_year = CustomerOrders.objects.filter(category_id=7, amount_paid__exact=0, date_added__gte=last_year)

    orders_blackmask_today = CustomerOrders.objects.filter(category_id=16, amount_paid__exact=0, date_added=today)
    orders_blackmask_yesterday = CustomerOrders.objects.filter(category_id=16, amount_paid__exact=0, date_added=yesterday)
    orders_blackmask_last_week = CustomerOrders.objects.filter(category_id=16, amount_paid__exact=0, date_added__gte=last_week)
    orders_blackmask_last_month = CustomerOrders.objects.filter(category_id=16, amount_paid__exact=0, date_added__gte=last_month)
    orders_blackmask_last_year = CustomerOrders.objects.filter(category_id=16, amount_paid__exact=0, date_added__gte=last_year)

    orders_tamtadu_today = CustomerOrders.objects.filter(category_id=17, amount_paid__exact=0, date_added=today)
    orders_tamtadu_yesterday = CustomerOrders.objects.filter(category_id=17, amount_paid__exact=0, date_added=yesterday)
    orders_tamtadu_last_week = CustomerOrders.objects.filter(category_id=17, amount_paid__exact=0, date_added__gte=last_week)
    orders_tamtadu_last_month = CustomerOrders.objects.filter(category_id=17, amount_paid__exact=0, date_added__gte=last_month)
    orders_tamtadu_last_year = CustomerOrders.objects.filter(category_id=17, amount_paid__exact=0, date_added__gte=last_year)

    orders_vagmint_today = CustomerOrders.objects.filter(category_id=18, amount_paid__exact=0, date_added=today)
    orders_vagmint_yesterday = CustomerOrders.objects.filter(category_id=18, amount_paid__exact=0, date_added=yesterday)
    orders_vagmint_last_week = CustomerOrders.objects.filter(category_id=18, amount_paid__exact=0, date_added__gte=last_week)
    orders_vagmint_last_month = CustomerOrders.objects.filter(category_id=18, amount_paid__exact=0, date_added__gte=last_month)
    orders_vagmint_last_year = CustomerOrders.objects.filter(category_id=18, amount_paid__exact=0, date_added__gte=last_year)

    orders_con_slimtea_today = CustomerOrders.objects.filter(category_id=1, date_paid=today).exclude(amount_paid=0)
    orders_con_slimtea_yesterday = CustomerOrders.objects.filter(category_id=1, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_slimtea_last_week = CustomerOrders.objects.filter(category_id=1, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_slimtea_last_month = CustomerOrders.objects.filter(category_id=1,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_slimtea_last_year = CustomerOrders.objects.filter(category_id=1, date_paid__gte=last_year).exclude(amount_paid=0)
    orders_con_waist_today = CustomerOrders.objects.filter(category_id=2,  date_paid=today).exclude(amount_paid=0)
    orders_con_waist_yesterday = CustomerOrders.objects.filter(category_id=2, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_waist_last_week = CustomerOrders.objects.filter(category_id=2,  date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_waist_last_month = CustomerOrders.objects.filter(category_id=2, date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_waist_last_year = CustomerOrders.objects.filter(category_id=2,  date_paid__gte=last_year).exclude(amount_paid=0)
    orders_con_mecran_today = CustomerOrders.objects.filter(category_id=3,  date_paid=today).exclude(amount_paid=0)
    orders_con_mecran_yesterday = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_mecran_last_week = CustomerOrders.objects.filter(category_id=3, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_mecran_last_month = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_mecran_last_year = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=last_year).exclude(amount_paid=0)
    orders_con_flattummy_today = CustomerOrders.objects.filter(category_id=4,  date_paid=today).exclude(amount_paid=0)
    orders_con_flattummy_yesterday = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_flattummy_last_week = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_flattummy_last_month = CustomerOrders.objects.filter(category_id=4, date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_flattummy_last_year = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_moolato_today = CustomerOrders.objects.filter(category_id=6, date_paid=today).exclude(amount_paid=0)
    orders_con_moolato_yesterday = CustomerOrders.objects.filter(category_id=6, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_moolato_last_week = CustomerOrders.objects.filter(category_id=6, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_moolato_last_month = CustomerOrders.objects.filter(category_id=6,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_moolato_last_year = CustomerOrders.objects.filter(category_id=6, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_hairnownow_today = CustomerOrders.objects.filter(category_id=5, date_paid=today).exclude(amount_paid=0)
    orders_con_hairnownow_yesterday = CustomerOrders.objects.filter(category_id=5, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_hairnownow_last_week = CustomerOrders.objects.filter(category_id=5, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_hairnownow_last_month = CustomerOrders.objects.filter(category_id=5,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_hairnownow_last_year = CustomerOrders.objects.filter(category_id=5, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_hairnymph_today = CustomerOrders.objects.filter(category_id=7, date_paid=today).exclude(amount_paid=0)
    orders_con_hairnymph_yesterday = CustomerOrders.objects.filter(category_id=7, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_hairnymph_last_week = CustomerOrders.objects.filter(category_id=7, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_hairnymph_last_month = CustomerOrders.objects.filter(category_id=7,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_hairnymph_last_year = CustomerOrders.objects.filter(category_id=7, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_blackmask_today = CustomerOrders.objects.filter(category_id=16, date_paid=today).exclude(amount_paid=0)
    orders_con_blackmask_yesterday = CustomerOrders.objects.filter(category_id=16, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_blackmask_last_week = CustomerOrders.objects.filter(category_id=16, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_blackmask_last_month = CustomerOrders.objects.filter(category_id=16,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_blackmask_last_year = CustomerOrders.objects.filter(category_id=16, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_tamtadu_today = CustomerOrders.objects.filter(category_id=17, date_paid=today).exclude(amount_paid=0)
    orders_con_tamtadu_yesterday = CustomerOrders.objects.filter(category_id=17, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_tamtadu_last_week = CustomerOrders.objects.filter(category_id=17, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_tamtadu_last_month = CustomerOrders.objects.filter(category_id=17,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_tamtadu_last_year = CustomerOrders.objects.filter(category_id=17, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_con_vagmint_today = CustomerOrders.objects.filter(category_id=18, date_paid=today).exclude(amount_paid=0)
    orders_con_vagmint_yesterday = CustomerOrders.objects.filter(category_id=18, date_paid__gte=yesterday).exclude(amount_paid=0)
    orders_con_vagmint_last_week = CustomerOrders.objects.filter(category_id=18, date_paid__gte=last_week).exclude(amount_paid=0)
    orders_con_vagmint_last_month = CustomerOrders.objects.filter(category_id=18,  date_paid__gte=last_month).exclude(amount_paid=0)
    orders_con_vagmint_last_year = CustomerOrders.objects.filter(category_id=18, date_paid__gte=last_year).exclude(amount_paid=0)

    orders_amt_slimtea_today = CustomerOrders.objects.filter(category_id=1, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_slimtea_yesterday = CustomerOrders.objects.filter(category_id=1, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_slimtea_last_week = CustomerOrders.objects.filter(category_id=1, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_slimtea_last_month = CustomerOrders.objects.filter(category_id=1,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_slimtea_last_year = CustomerOrders.objects.filter(category_id=1, date_paid__gte=last_year).aggregate(Sum('amount_paid'))
    orders_amt_waist_today = CustomerOrders.objects.filter(category_id=2,  date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_waist_yesterday = CustomerOrders.objects.filter(category_id=2, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_waist_last_week = CustomerOrders.objects.filter(category_id=2,  date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_waist_last_month = CustomerOrders.objects.filter(category_id=2, date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_waist_last_year = CustomerOrders.objects.filter(category_id=2,  date_paid__gte=last_year).aggregate(Sum('amount_paid'))
    orders_amt_mecran_today = CustomerOrders.objects.filter(category_id=3,  date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_mecran_yesterday = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_mecran_last_week = CustomerOrders.objects.filter(category_id=3, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_mecran_last_month = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_mecran_last_year = CustomerOrders.objects.filter(category_id=3,  date_paid__gte=last_year).aggregate(Sum('amount_paid'))
    orders_amt_flattummy_today = CustomerOrders.objects.filter(category_id=4,  date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_flattummy_yesterday = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_flattummy_last_week = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_flattummy_last_month = CustomerOrders.objects.filter(category_id=4, date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_flattummy_last_year = CustomerOrders.objects.filter(category_id=4,  date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_moolato_today = CustomerOrders.objects.filter(category_id=6, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_moolato_yesterday = CustomerOrders.objects.filter(category_id=6, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_moolato_last_week = CustomerOrders.objects.filter(category_id=6, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_moolato_last_month = CustomerOrders.objects.filter(category_id=6,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_moolato_last_year = CustomerOrders.objects.filter(category_id=6, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_hairnownow_today = CustomerOrders.objects.filter(category_id=5, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_hairnownow_yesterday = CustomerOrders.objects.filter(category_id=5, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_hairnownow_last_week = CustomerOrders.objects.filter(category_id=5, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_hairnownow_last_month = CustomerOrders.objects.filter(category_id=5,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_hairnownow_last_year = CustomerOrders.objects.filter(category_id=5, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_hairnymph_today = CustomerOrders.objects.filter(category_id=7, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_hairnymph_yesterday = CustomerOrders.objects.filter(category_id=7, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_hairnymph_last_week = CustomerOrders.objects.filter(category_id=7, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_hairnymph_last_month = CustomerOrders.objects.filter(category_id=7,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_hairnymph_last_year = CustomerOrders.objects.filter(category_id=7, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_blackmask_today = CustomerOrders.objects.filter(category_id=16, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_blackmask_yesterday = CustomerOrders.objects.filter(category_id=16, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_blackmask_last_week = CustomerOrders.objects.filter(category_id=16, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_blackmask_last_month = CustomerOrders.objects.filter(category_id=16,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_blackmask_last_year = CustomerOrders.objects.filter(category_id=16, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_tamtadu_today = CustomerOrders.objects.filter(category_id=17, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_tamtadu_yesterday = CustomerOrders.objects.filter(category_id=17, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_tamtadu_last_week = CustomerOrders.objects.filter(category_id=17, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_tamtadu_last_month = CustomerOrders.objects.filter(category_id=17,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_tamtadu_last_year = CustomerOrders.objects.filter(category_id=17, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_amt_vagmint_today = CustomerOrders.objects.filter(category_id=18, date_paid=today).aggregate(Sum('amount_paid'))
    orders_amt_vagmint_yesterday = CustomerOrders.objects.filter(category_id=18, date_paid__gte=yesterday).aggregate(Sum('amount_paid'))
    orders_amt_vagmint_last_week = CustomerOrders.objects.filter(category_id=18, date_paid__gte=last_week).aggregate(Sum('amount_paid'))
    orders_amt_vagmint_last_month = CustomerOrders.objects.filter(category_id=18,  date_paid__gte=last_month).aggregate(Sum('amount_paid'))
    orders_amt_vagmint_last_year = CustomerOrders.objects.filter(category_id=18, date_paid__gte=last_year).aggregate(Sum('amount_paid'))

    orders_ptv_slimtea_today = CustomerOrders.objects.filter(category_id=1, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_slimtea_yesterday = CustomerOrders.objects.filter(category_id=1, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_slimtea_last_week = CustomerOrders.objects.filter(category_id=1, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_slimtea_last_month = CustomerOrders.objects.filter(category_id=1,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_slimtea_last_year = CustomerOrders.objects.filter(category_id=1, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_waist_today = CustomerOrders.objects.filter(category_id=2,  date_added=today).aggregate(Sum('product_value'))
    orders_ptv_waist_yesterday = CustomerOrders.objects.filter(category_id=2, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_waist_last_week = CustomerOrders.objects.filter(category_id=2,  date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_waist_last_month = CustomerOrders.objects.filter(category_id=2, date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_waist_last_year = CustomerOrders.objects.filter(category_id=2,  date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_mecran_today = CustomerOrders.objects.filter(category_id=3,  date_added=today).aggregate(Sum('product_value'))
    orders_ptv_mecran_yesterday = CustomerOrders.objects.filter(category_id=3,  date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_mecran_last_week = CustomerOrders.objects.filter(category_id=3, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_mecran_last_month = CustomerOrders.objects.filter(category_id=3,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_mecran_last_year = CustomerOrders.objects.filter(category_id=3,  date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_flattummy_today = CustomerOrders.objects.filter(category_id=4,  date_added=today).aggregate(Sum('product_value'))
    orders_ptv_flattummy_yesterday = CustomerOrders.objects.filter(category_id=4,  date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_flattummy_last_week = CustomerOrders.objects.filter(category_id=4,  date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_flattummy_last_month = CustomerOrders.objects.filter(category_id=4, date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_flattummy_last_year = CustomerOrders.objects.filter(category_id=4,  date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_moolato_today = CustomerOrders.objects.filter(category_id=6, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_moolato_yesterday = CustomerOrders.objects.filter(category_id=6, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_moolato_last_week = CustomerOrders.objects.filter(category_id=6, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_moolato_last_month = CustomerOrders.objects.filter(category_id=6,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_moolato_last_year = CustomerOrders.objects.filter(category_id=6, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_hairnownow_today = CustomerOrders.objects.filter(category_id=5, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_hairnownow_yesterday = CustomerOrders.objects.filter(category_id=5, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_hairnownow_last_week = CustomerOrders.objects.filter(category_id=5, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_hairnownow_last_month = CustomerOrders.objects.filter(category_id=5,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_hairnownow_last_year = CustomerOrders.objects.filter(category_id=5, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_hairnymph_today = CustomerOrders.objects.filter(category_id=7, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_hairnymph_yesterday = CustomerOrders.objects.filter(category_id=7, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_hairnymph_last_week = CustomerOrders.objects.filter(category_id=7, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_hairnymph_last_month = CustomerOrders.objects.filter(category_id=7,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_hairnymph_last_year = CustomerOrders.objects.filter(category_id=7, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_blackmask_today = CustomerOrders.objects.filter(category_id=16, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_blackmask_yesterday = CustomerOrders.objects.filter(category_id=16, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_blackmask_last_week = CustomerOrders.objects.filter(category_id=16, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_blackmask_last_month = CustomerOrders.objects.filter(category_id=16,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_blackmask_last_year = CustomerOrders.objects.filter(category_id=16, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_tamtadu_today = CustomerOrders.objects.filter(category_id=17, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_yesterday = CustomerOrders.objects.filter(category_id=17, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_week = CustomerOrders.objects.filter(category_id=17, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_month = CustomerOrders.objects.filter(category_id=17,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_year = CustomerOrders.objects.filter(category_id=17, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_tamtadu_today = CustomerOrders.objects.filter(category_id=17, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_yesterday = CustomerOrders.objects.filter(category_id=17, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_week = CustomerOrders.objects.filter(category_id=17, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_month = CustomerOrders.objects.filter(category_id=17,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_tamtadu_last_year = CustomerOrders.objects.filter(category_id=17, date_added__gte=last_year).aggregate(Sum('product_value'))

    orders_ptv_vagmint_today = CustomerOrders.objects.filter(category_id=18, date_added=today).aggregate(Sum('product_value'))
    orders_ptv_vagmint_yesterday = CustomerOrders.objects.filter(category_id=18, date_added=yesterday).aggregate(Sum('product_value'))
    orders_ptv_vagmint_last_week = CustomerOrders.objects.filter(category_id=18, date_added__gte=last_week).aggregate(Sum('product_value'))
    orders_ptv_vagmint_last_month = CustomerOrders.objects.filter(category_id=18,  date_added__gte=last_month).aggregate(Sum('product_value'))
    orders_ptv_vagmint_last_year = CustomerOrders.objects.filter(category_id=18, date_added__gte=last_year).aggregate(Sum('product_value'))

    entry_orders_count_today = User.objects.filter(groups__name='entry').filter(customerorders__date_added=today).annotate(number_of_orders=Count('customerorders', distinct=True)).annotate(total_product_value=Sum('customerorders__product_value')).values("username", "number_of_orders", "total_product_value")
    entry_orders_count_yesterday = User.objects.filter(groups__name='entry').filter(customerorders__date_added=yesterday).annotate(number_of_orders=Count('customerorders', distinct=True)).annotate(total_product_value=Sum('customerorders__product_value')).values("username", "number_of_orders", "total_product_value")
    entry_orders_count_week = User.objects.filter(groups__name='entry').filter(customerorders__date_added__gte=last_week).annotate(number_of_orders=Count('customerorders', distinct=True)).annotate(total_product_value=Sum('customerorders__product_value')).values("username", "number_of_orders", "total_product_value")
    entry_orders_count_all = User.objects.filter(groups__name='entry').annotate(number_of_orders=Count('customerorders', distinct=True)).annotate(total_product_value=Sum('customerorders__product_value')).values("username", "number_of_orders", "total_product_value")





    return render(request, 'inventory/index.html', {'orders_slimtea': orders_slimtea_today,
                                                    'orders_slimtea_y': orders_slimtea_yesterday,
                                                    'orders_slimtea_w': orders_slimtea_last_week,
                                                    'orders_slimtea_m': orders_slimtea_last_month,
                                                    'orders_slimtea_year': orders_slimtea_last_year,
                                                    'orders_waist': orders_waist_today,
                                                    'orders_waist_y': orders_waist_yesterday,
                                                    'orders_waist_w': orders_waist_last_week,
                                                    'orders_waist_m': orders_waist_last_month,
                                                    'orders_waist_year': orders_waist_last_year,
                                                    'orders_mecran': orders_mecran_today,
                                                    'orders_mecran_y': orders_mecran_yesterday,
                                                    'orders_mecran_w': orders_mecran_last_week,
                                                    'orders_mecran_m': orders_mecran_last_month,
                                                    'orders_mecran_year': orders_mecran_last_year,
                                                    'orders_flattummy': orders_flattummy_today,
                                                    'orders_flattummy_y': orders_flattummy_yesterday,
                                                    'orders_flattummy_w': orders_flattummy_last_week,
                                                    'orders_flattummy_m': orders_flattummy_last_month,
                                                    'orders_flattummy_year': orders_flattummy_last_year,

                                                    'orders_moolato': orders_moolato_today,
                                                    'orders_moolato_y': orders_moolato_yesterday,
                                                    'orders_moolato_w': orders_moolato_last_week,
                                                    'orders_moolato_m': orders_moolato_last_month,
                                                    'orders_moolato_year': orders_moolato_last_year,

                                                    'orders_hairnownow': orders_hairnownow_today,
                                                    'orders_hairnownow_y': orders_hairnownow_yesterday,
                                                    'orders_hairnownow_w': orders_hairnownow_last_week,
                                                    'orders_hairnownow_m': orders_hairnownow_last_month,
                                                    'orders_hairnownow_year': orders_hairnownow_last_year,

                                                    'orders_hairnymph': orders_hairnymph_today,
                                                    'orders_hairnymph_y': orders_hairnymph_yesterday,
                                                    'orders_hairnymph_w': orders_hairnymph_last_week,
                                                    'orders_hairnymph_m': orders_hairnymph_last_month,
                                                    'orders_hairnymph_year': orders_hairnymph_last_year,

                                                    'orders_blackmask': orders_blackmask_today,
                                                    'orders_blackmask_y': orders_blackmask_yesterday,
                                                    'orders_blackmask_w': orders_blackmask_last_week,
                                                    'orders_blackmask_m': orders_blackmask_last_month,
                                                    'orders_blackmask_year': orders_blackmask_last_year,

                                                    'orders_tamtadu': orders_tamtadu_today,
                                                    'orders_tamtadu_y': orders_tamtadu_yesterday,
                                                    'orders_tamtadu_w': orders_tamtadu_last_week,
                                                    'orders_tamtadu_m': orders_tamtadu_last_month,
                                                    'orders_tamtadu_year': orders_tamtadu_last_year,

                                                    'orders_vagmint': orders_vagmint_today,
                                                    'orders_vagmint_y': orders_vagmint_yesterday,
                                                    'orders_vagmint_w': orders_vagmint_last_week,
                                                    'orders_vagmint_m': orders_vagmint_last_month,
                                                    'orders_vagmint_year': orders_vagmint_last_year,

                                                    'orders_con_slimtea': orders_con_slimtea_today,
                                                    'orders_con_slimtea_y': orders_con_slimtea_yesterday,
                                                    'orders_con_slimtea_w': orders_con_slimtea_last_week,
                                                    'orders_con_slimtea_m': orders_con_slimtea_last_month,
                                                    'orders_con_slimtea_year': orders_con_slimtea_last_year,
                                                    'orders_con_waist': orders_con_waist_today,
                                                    'orders_con_waist_y': orders_con_waist_yesterday,
                                                    'orders_con_waist_w': orders_con_waist_last_week,
                                                    'orders_con_waist_m': orders_con_waist_last_month,
                                                    'orders_con_waist_year': orders_con_waist_last_year,
                                                    'orders_con_mecran': orders_con_mecran_today,
                                                    'orders_con_mecran_y': orders_con_mecran_yesterday,
                                                    'orders_con_mecran_w': orders_con_mecran_last_week,
                                                    'orders_con_mecran_m': orders_con_mecran_last_month,
                                                    'orders_con_mecran_year': orders_con_mecran_last_year,
                                                    'orders_con_flattummy': orders_con_flattummy_today,
                                                    'orders_con_flattummy_y': orders_con_flattummy_yesterday,
                                                    'orders_con_flattummy_w': orders_con_flattummy_last_week,
                                                    'orders_con_flattummy_m': orders_con_flattummy_last_month,
                                                    'orders_con_flattummy_year': orders_con_flattummy_last_year,

                                                    'orders_con_moolato': orders_con_moolato_today,
                                                    'orders_con_moolato_y': orders_con_moolato_yesterday,
                                                    'orders_con_moolato_w': orders_con_moolato_last_week,
                                                    'orders_con_moolato_m': orders_con_moolato_last_month,
                                                    'orders_con_moolato_year': orders_con_moolato_last_year,

                                                    'orders_con_hairnownow': orders_con_hairnownow_today,
                                                    'orders_con_hairnownow_y': orders_con_hairnownow_yesterday,
                                                    'orders_con_hairnownow_w': orders_con_hairnownow_last_week,
                                                    'orders_con_hairnownow_m': orders_con_hairnownow_last_month,
                                                    'orders_con_hairnownow_year': orders_con_hairnownow_last_year,

                                                    'orders_con_hairnymph': orders_con_hairnymph_today,
                                                    'orders_con_hairnymph_y': orders_con_hairnymph_yesterday,
                                                    'orders_con_hairnymph_w': orders_con_hairnymph_last_week,
                                                    'orders_con_hairnymph_m': orders_con_hairnymph_last_month,
                                                    'orders_con_hairnymph_year': orders_con_hairnymph_last_year,

                                                    'orders_con_blackmask': orders_con_blackmask_today,
                                                    'orders_con_blackmask_y': orders_con_blackmask_yesterday,
                                                    'orders_con_blackmask_w': orders_con_blackmask_last_week,
                                                    'orders_con_blackmask_m': orders_con_blackmask_last_month,
                                                    'orders_con_blackmask_year': orders_con_blackmask_last_year,

                                                    'orders_con_tamtadu': orders_con_tamtadu_today,
                                                    'orders_con_tamtadu_y': orders_con_tamtadu_yesterday,
                                                    'orders_con_tamtadu_w': orders_con_tamtadu_last_week,
                                                    'orders_con_tamtadu_m': orders_con_tamtadu_last_month,
                                                    'orders_con_tamtadu_year': orders_con_tamtadu_last_year,

                                                    'orders_con_vagmint': orders_con_vagmint_today,
                                                    'orders_con_vagmint_y': orders_con_vagmint_yesterday,
                                                    'orders_con_vagmint_w': orders_con_vagmint_last_week,
                                                    'orders_con_vagmint_m': orders_con_vagmint_last_month,
                                                    'orders_con_vagmint_year': orders_con_vagmint_last_year,

                                                    'orders_amt_slimtea': orders_amt_slimtea_today,
                                                    'orders_amt_slimtea_y': orders_amt_slimtea_yesterday,
                                                    'orders_amt_slimtea_w': orders_amt_slimtea_last_week,
                                                    'orders_amt_slimtea_m': orders_amt_slimtea_last_month,
                                                    'orders_amt_slimtea_year': orders_amt_slimtea_last_year,
                                                    'orders_amt_waist': orders_amt_waist_today,
                                                    'orders_amt_waist_y': orders_amt_waist_yesterday,
                                                    'orders_amt_waist_w': orders_amt_waist_last_week,
                                                    'orders_amt_waist_m': orders_amt_waist_last_month,
                                                    'orders_amt_waist_year': orders_amt_waist_last_year,
                                                    'orders_amt_mecran': orders_amt_mecran_today,
                                                    'orders_amt_mecran_y': orders_amt_mecran_yesterday,
                                                    'orders_amt_mecran_w': orders_amt_mecran_last_week,
                                                    'orders_amt_mecran_m': orders_amt_mecran_last_month,
                                                    'orders_amt_mecran_year': orders_amt_mecran_last_year,
                                                    'orders_amt_flattummy': orders_amt_flattummy_today,
                                                    'orders_amt_flattummy_y': orders_amt_flattummy_yesterday,
                                                    'orders_amt_flattummy_w': orders_amt_flattummy_last_week,
                                                    'orders_amt_flattummy_m': orders_amt_flattummy_last_month,
                                                    'orders_amt_flattummy_year': orders_amt_flattummy_last_year,

                                                    'orders_amt_moolato': orders_amt_moolato_today,
                                                    'orders_amt_moolato_y': orders_amt_moolato_yesterday,
                                                    'orders_amt_moolato_w': orders_amt_moolato_last_week,
                                                    'orders_amt_moolato_m': orders_amt_moolato_last_month,
                                                    'orders_amt_moolato_year': orders_amt_moolato_last_year,

                                                    'orders_amt_hairnownow': orders_amt_hairnownow_today,
                                                    'orders_amt_hairnownow_y': orders_amt_hairnownow_yesterday,
                                                    'orders_amt_hairnownow_w': orders_amt_hairnownow_last_week,
                                                    'orders_amt_hairnownow_m': orders_amt_hairnownow_last_month,
                                                    'orders_amt_hairnownow_year': orders_amt_hairnownow_last_year,

                                                    'orders_amt_hairnymph': orders_amt_hairnymph_today,
                                                    'orders_amt_hairnymph_y': orders_amt_hairnymph_yesterday,
                                                    'orders_amt_hairnymph_w': orders_amt_hairnymph_last_week,
                                                    'orders_amt_hairnymph_m': orders_amt_hairnymph_last_month,
                                                    'orders_amt_hairnymph_year': orders_amt_hairnymph_last_year,

                                                    'orders_amt_blackmask': orders_amt_blackmask_today,
                                                    'orders_amt_blackmask_y': orders_amt_blackmask_yesterday,
                                                    'orders_amt_blackmask_w': orders_amt_blackmask_last_week,
                                                    'orders_amt_blackmask_m': orders_amt_blackmask_last_month,
                                                    'orders_amt_blackmask_year': orders_amt_blackmask_last_year,

                                                    'orders_amt_tamtadu': orders_amt_tamtadu_today,
                                                    'orders_amt_tamtadu_y': orders_amt_tamtadu_yesterday,
                                                    'orders_amt_tamtadu_w': orders_amt_tamtadu_last_week,
                                                    'orders_amt_tamtadu_m': orders_amt_tamtadu_last_month,
                                                    'orders_amt_tamtadu_year': orders_amt_tamtadu_last_year,

                                                    'orders_amt_vagmint': orders_amt_vagmint_today,
                                                    'orders_amt_vagmint_y': orders_amt_vagmint_yesterday,
                                                    'orders_amt_vagmint_w': orders_amt_vagmint_last_week,
                                                    'orders_amt_vagmint_m': orders_amt_vagmint_last_month,
                                                    'orders_amt_vagmint_year': orders_amt_vagmint_last_year,

                                                    'orders_ptv_slimtea': orders_ptv_slimtea_today,
                                                    'orders_ptv_slimtea_y': orders_ptv_slimtea_yesterday,
                                                    'orders_ptv_slimtea_w': orders_ptv_slimtea_last_week,
                                                    'orders_ptv_slimtea_m': orders_ptv_slimtea_last_month,
                                                    'orders_ptv_slimtea_year': orders_ptv_slimtea_last_year,
                                                    'orders_ptv_waist': orders_ptv_waist_today,
                                                    'orders_ptv_waist_y': orders_ptv_waist_yesterday,
                                                    'orders_ptv_waist_w': orders_ptv_waist_last_week,
                                                    'orders_ptv_waist_m': orders_ptv_waist_last_month,
                                                    'orders_ptv_waist_year': orders_ptv_waist_last_year,
                                                    'orders_ptv_mecran': orders_ptv_mecran_today,
                                                    'orders_ptv_mecran_y': orders_ptv_mecran_yesterday,
                                                    'orders_ptv_mecran_w': orders_ptv_mecran_last_week,
                                                    'orders_ptv_mecran_m': orders_ptv_mecran_last_month,
                                                    'orders_ptv_mecran_year': orders_ptv_mecran_last_year,
                                                    'orders_ptv_flattummy': orders_ptv_flattummy_today,
                                                    'orders_ptv_flattummy_y': orders_ptv_flattummy_yesterday,
                                                    'orders_ptv_flattummy_w': orders_ptv_flattummy_last_week,
                                                    'orders_ptv_flattummy_m': orders_ptv_flattummy_last_month,
                                                    'orders_ptv_flattummy_year': orders_ptv_flattummy_last_year,

                                                    'orders_ptv_moolato': orders_ptv_moolato_today,
                                                    'orders_ptv_moolato_y': orders_ptv_moolato_yesterday,
                                                    'orders_ptv_moolato_w': orders_ptv_moolato_last_week,
                                                    'orders_ptv_moolato_m': orders_ptv_moolato_last_month,
                                                    'orders_ptv_moolato_year': orders_ptv_moolato_last_year,

                                                    'orders_ptv_hairnownow': orders_ptv_hairnownow_today,
                                                    'orders_ptv_hairnownow_y': orders_ptv_hairnownow_yesterday,
                                                    'orders_ptv_hairnownow_w': orders_ptv_hairnownow_last_week,
                                                    'orders_ptv_hairnownow_m': orders_ptv_hairnownow_last_month,
                                                    'orders_ptv_hairnownow_year': orders_ptv_hairnownow_last_year,

                                                    'orders_ptv_hairnymph': orders_ptv_hairnymph_today,
                                                    'orders_ptv_hairnymph_y': orders_ptv_hairnymph_yesterday,
                                                    'orders_ptv_hairnymph_w': orders_ptv_hairnymph_last_week,
                                                    'orders_ptv_hairnymph_m': orders_ptv_hairnymph_last_month,
                                                    'orders_ptv_hairnymph_year': orders_ptv_hairnymph_last_year,

                                                    'orders_ptv_blackmask': orders_ptv_blackmask_today,
                                                    'orders_ptv_blackmask_y': orders_ptv_blackmask_yesterday,
                                                    'orders_ptv_blackmask_w': orders_ptv_blackmask_last_week,
                                                    'orders_ptv_blackmask_m': orders_ptv_blackmask_last_month,
                                                    'orders_ptv_blackmask_year': orders_ptv_blackmask_last_year,

                                                    'orders_ptv_blackmask': orders_ptv_blackmask_today,
                                                    'orders_ptv_blackmask_y': orders_ptv_blackmask_yesterday,
                                                    'orders_ptv_blackmask_w': orders_ptv_blackmask_last_week,
                                                    'orders_ptv_blackmask_m': orders_ptv_blackmask_last_month,
                                                    'orders_ptv_blackmask_year': orders_ptv_blackmask_last_year,

                                                    'orders_ptv_blackmask': orders_ptv_blackmask_today,
                                                    'orders_ptv_blackmask_y': orders_ptv_blackmask_yesterday,
                                                    'orders_ptv_blackmask_w': orders_ptv_blackmask_last_week,
                                                    'orders_ptv_blackmask_m': orders_ptv_blackmask_last_month,
                                                    'orders_ptv_blackmask_year': orders_ptv_blackmask_last_year,

                                                    'orders_ptv_tamtadu': orders_ptv_tamtadu_today,
                                                    'orders_ptv_tamtadu_y': orders_ptv_tamtadu_yesterday,
                                                    'orders_ptv_tamtadu_w': orders_ptv_tamtadu_last_week,
                                                    'orders_ptv_tamtadu_m': orders_ptv_tamtadu_last_month,
                                                    'orders_ptv_tamtadu_year': orders_ptv_tamtadu_last_year,

                                                    'orders_ptv_vagmint': orders_ptv_vagmint_today,
                                                    'orders_ptv_vagmint_y': orders_ptv_vagmint_yesterday,
                                                    'orders_ptv_vagmint_w': orders_ptv_vagmint_last_week,
                                                    'orders_ptv_vagmint_m': orders_ptv_vagmint_last_month,
                                                    'orders_ptv_vagmint_year': orders_ptv_vagmint_last_year,

                                                    'categories': categories,
                                                    'is_dperson': is_dperson,
                                                    'is_entry': is_entry,
                                                    'is_lagos': is_lagos,
                                                    'is_daily': is_daily,
                                                    'is_vieworders': is_vieworders,
                                                    'is_comsexec': is_comsexec,
                                                    'is_stock': is_stock,
                                                    'is_orderstatus': is_orderstatus,
                                                    'user_orders': user_orders,
                                                    'user_processed_orders': user_processed_orders,
                                                    'user_coms_today_product_value': user_coms_today_product_value,
                                                    'user_coms_all_product_value': user_coms_all_product_value,
                                                    'user_coms_all_amount_paid': user_coms_all_amount_paid,
                                                    'user_coms_week_amount_paid': user_coms_week_amount_paid,
                                                    'com_orders': coms_orders,
                                                    'com_orders_today': coms_orders_today,
                                                    'com_orders_yesterday': coms_orders_yesterday,
                                                    'com_orders_w': coms_orders_last_week,
                                                    'com_orders_m': coms_orders_last_month,
                                                    'com_orders_y': coms_orders_last_year,

                                                    'entry_orders_count_today': entry_orders_count_today,
                                                    'entry_orders_count_yesterday': entry_orders_count_yesterday,
                                                    'entry_orders_count_week': entry_orders_count_week,
                                                    'entry_orders_count_all': entry_orders_count_all,
                                                    })


@login_required
def new_customer_order(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    coms_reps = ComsReps.objects.all()
    cat = Category.objects.get(id=id)
    my_form = CustomerOrderForm(cat)
    if request.method == 'POST':
        form = CustomerOrderForm(cat, request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.category = cat
            customer.save()
            form = my_form
            messages.success(request, category + ' Customer Order Created Successfully, You can Add Another Order')
            return render(request, 'inventory/new_customer_order.html', {'form': form, 'category': category,
                                                                         'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily,})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Order Form')
    else:
        form = my_form
    return render(request, 'inventory/new_customer_order.html', {
        'form': form, 'category': category, 'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily,
    })


@login_required
def lagos_new_customer_order(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    coms_reps = ComsReps.objects.all()
    cat = Category.objects.get(id=id)
    my_form = LagosCustomerOrderForm(cat)
    if request.method == 'POST':
        form = LagosCustomerOrderForm(cat, request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.category = cat
            customer.save()
            form = my_form
            messages.success(request, category + ' Customer Order Created Successfully, You can Add Another Order')
            return render(request, 'inventory/new_customer_order.html', {'form': form, 'category': category,
                                                                         'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily,})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Order Form')
    else:
        form = my_form
    return render(request, 'inventory/new_customer_order.html', {
        'form': form, 'category': category, 'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily,
    })


@login_required
def orders(request, category, id):
    if 'start_date' in request.GET:
        s_date = request.GET['start_date']
        e_date = request.GET['end_date']
        all_orders = CustomerOrders.objects.filter(date__range=[s_date, e_date], category_id=id).order_by('-date', '-time')
    else:
        all_orders = CustomerOrders.objects.filter(category_id=id).order_by('-date', '-time')
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    categories = Category.objects.all()
    paginator = Paginator(all_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': all_orders, 'category': category,
                                                     'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})


@login_required
def ajax_user_search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            results = CustomerOrders.objects.filter(
                Q(cust_name__contains=q) |
                Q(phone_no__contains=q) |
                Q(date_added__contains=q) |
                Q(state__contains=q)
                ).order_by('cust_name')

            template = 'inventory/results.html'
            data = {
                'results': results,
            }
            return render(request, template, data)


@login_required
def order(request, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    is_comsexec = request.user.groups.filter(name='comsexec').exists()
    order_details = CustomerOrders.objects.get(id=id)
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    categories = Category.objects.all()
    return render(request, 'inventory/order.html', {'order_details': order_details, 'categories': categories, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders, 'is_comsexec': is_comsexec, 'is_orderstatus': is_orderstatus})


@login_required
def edit_customer_order(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    coms_reps = ComsReps.objects.all()
    cat = Category.objects.filter(name__startswith=category)
    edit_order = CustomerOrders.objects.get(id=id)
    my_form = CustomerOrderForm(cat)
    if request.method == 'POST':
        form = CustomerOrderForm(cat, request.POST, instance=edit_order)
        if form.is_valid():
            form.save()
            form = CustomerOrderForm(cat, instance=edit_order)
            messages.success(request, category + ' Customer Order Edited Successfully')
            return render(request, 'inventory/new_customer_order.html', {'form': form, 'category': category,
                                                                         'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Order Form')
    else:
        form = CustomerOrderForm(cat, instance=edit_order)
    return render(request, 'inventory/new_customer_order.html', {
        'form': form, 'category': category, 'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry,
    })

@login_required
def confirm_order(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    categories = Category.objects.all()
    coms_reps = ComsReps.objects.all()
    cat = Category.objects.filter(name__startswith=category)
    edit_order = CustomerOrders.objects.get(id=id)
    my_form = ConfirmCustomerOrderForm(cat)
    if request.method == 'POST':
        form = ConfirmCustomerOrderForm(cat, request.POST, instance=edit_order)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.order_status = "DELIVERED"
            customer.save()
            form = ConfirmCustomerOrderForm(cat, instance=edit_order)
            messages.success(request, category + ' Customer Order Confirmed Successfully')
            return render(request, 'inventory/confirm_order.html', {'form': form, 'category': category,
                                                                         'categories': categories,
                                                                         'coms_reps': coms_reps, 'is_entry': is_entry, 'is_lagos': is_lagos, 'is_orderstatus': is_orderstatus,
                                                    'is_daily': is_daily})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Order Form')
    else:
        form = ConfirmCustomerOrderForm(cat, instance=edit_order)
    return render(request, 'inventory/confirm_order.html', {
        'form': form, 'category': category, 'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry,
    })


@login_required
def confirmed_orders(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    all_orders = CustomerOrders.objects.filter(category_id=id).exclude(amount_paid=0).order_by('-date_paid', '-time')
    paginator = Paginator(all_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/confirmed_orders.html', {'orders': all_orders, 'category': category,
                                                     'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily})


@login_required
def lagos_orders(request):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    lagos_orders = CustomerOrders.objects.filter(state__in=['lagos','Ogba', 'Festac', 'Aguda/Surulere', 'Ketu', 'VI', 'Ikotun', 'Oshodi', 'Ikeja', 'Lekki', 'Apapa']).order_by('-date', '-time').exclude(order_status="READY")
    paginator = Paginator(lagos_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/lagos_orders.html', {'orders': lagos_orders,
                                                               'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily})


@login_required
def ready_lagos_orders(request):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()

    if 'location' in request.GET:
        location = request.GET['location']
        lagos_orders = CustomerOrders.objects.filter(order_status="READY", state=location).order_by('-date', '-time')
    else:
        location = None
        lagos_orders = CustomerOrders.objects.filter(order_status="READY", state__in=['lagos','Ogba', 'Festac', 'Aguda/Surulere', 'Ketu', 'VI', 'Ikotun', 'Oshodi', 'Ikeja', 'Lekki', 'Apapa']).order_by('-date', '-time')
    paginator = Paginator(lagos_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/lagos_orders.html', {'orders': lagos_orders,
                                                               'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily})



@login_required
def ready_lagos_orders_print(request):
    if 'location' in request.GET:
        location = request.GET['location']
        lagos_orders = CustomerOrders.objects.filter(order_status="READY", state=location).order_by('-date', '-time')
    else:
        location = None
        lagos_orders = CustomerOrders.objects.filter(order_status="READY", state__in=['lagos','Ogba', 'Festac', 'Aguda/Surulere', 'Ketu', 'VI', 'Ikotun', 'Oshodi', 'Ikeja', 'Lekki', 'Apapa']).order_by('-date', '-time')
    html_template = get_template('inventory/ready_lagos_orders_print.html')
    rendered_html = html_template.render(RequestContext(request, {'lagos_orders': lagos_orders}))
    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css')])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename=' + str(today) +"Ready Lagos Orders By State.pdf"

    return http_response



@login_required
def non_lagos_orders(request):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()
    non_lagos_orders = CustomerOrders.objects.exclude(state="lagos").filter(category_id=4,date__range=["2017-03-20", "2017-03-28"]).order_by('-date')
    #paginator = Paginator(non_lagos_orders, 10)
    #page = request.GET.get('page')
    #try:
        #orderss = paginator.page(page)
    #except PageNotAnInteger:
       # orderss = paginator.page(1)
    #except EmptyPage:
        #orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/non_lagos_orders.html', {'orders': non_lagos_orders,
                                                               'categories': categories, 'orderss': non_lagos_orders, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily})

@login_required
def daily_orders(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()

    product_value_total = CustomerOrders.objects.filter(category_id=id, date_added=today).aggregate(Sum('product_value'))

    t_orders_Jakande = CustomerOrders.objects.filter(category_id=id, state='Jakande', date_added=today).aggregate(Sum('product_value'))
    t_orders_Sangotedo = CustomerOrders.objects.filter(category_id=id, state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    t_orders_Eleko = CustomerOrders.objects.filter(category_id=id, state='Eleko', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ajah = CustomerOrders.objects.filter(category_id=id, state='Ajah', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ogba = CustomerOrders.objects.filter(category_id=id, state='Ogba', date_added=today).aggregate(Sum('product_value'))
    t_orders_Aguda = CustomerOrders.objects.filter(category_id=id, state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ketu = CustomerOrders.objects.filter(category_id=id, state='Ketu', date_added=today).aggregate(Sum('product_value'))
    t_orders_VI = CustomerOrders.objects.filter(category_id=id, state='VI', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikotun = CustomerOrders.objects.filter( category_id=id,state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    t_orders_Oshodi = CustomerOrders.objects.filter(category_id=id, state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikeja = CustomerOrders.objects.filter(category_id=id, state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    t_orders_Lekki = CustomerOrders.objects.filter(category_id=id, state='Lekki', date_added=today).aggregate(Sum('product_value'))
    t_orders_Apapa = CustomerOrders.objects.filter(category_id=id, state='Apapa', date_added=today).aggregate(Sum('product_value'))

    t_orders_abia = CustomerOrders.objects.filter(category_id=id, state='abia', date_added=today).aggregate(Sum('product_value'))
    t_orders_adamawa = CustomerOrders.objects.filter(category_id=id, state='adamawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_anambra = CustomerOrders.objects.filter(category_id=id, state='anambra', date_added=today).aggregate(Sum('product_value'))
    t_orders_akwa_ibom = CustomerOrders.objects.filter(category_id=id, state='akwa-ibom', date_added=today).aggregate(Sum('product_value'))
    t_orders_bauchi = CustomerOrders.objects.filter(category_id=id, state='bauchi', date_added=today).aggregate(Sum('product_value'))
    t_orders_bayelsa = CustomerOrders.objects.filter(category_id=id, state='bayelsa', date_added=today).aggregate(Sum('product_value'))
    t_orders_benue = CustomerOrders.objects.filter(category_id=id, state='benue', date_added=today).aggregate(Sum('product_value'))
    t_orders_borno = CustomerOrders.objects.filter(category_id=id, state='borno', date_added=today).aggregate(Sum('product_value'))
    t_orders_cross_river = CustomerOrders.objects.filter(category_id=id, state='cross-river', date_added=today).aggregate(Sum('product_value'))
    t_orders_delta = CustomerOrders.objects.filter(category_id=id, state='delta', date_added=today).aggregate(Sum('product_value'))
    t_orders_ebonyi = CustomerOrders.objects.filter(category_id=id, state='ebonyi', date_added=today).aggregate(Sum('product_value'))
    t_orders_enugu = CustomerOrders.objects.filter(category_id=id, state='enugu', date_added=today).aggregate(Sum('product_value'))
    t_orders_edo = CustomerOrders.objects.filter(category_id=id, state='edo', date_added=today).aggregate(Sum('product_value'))
    t_orders_ekiti = CustomerOrders.objects.filter(category_id=id, state='ekiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_gombe = CustomerOrders.objects.filter(category_id=id, state='gombe', date_added=today).aggregate(Sum('product_value'))
    t_orders_imo = CustomerOrders.objects.filter(category_id=id, state='imo', date_added=today).aggregate(Sum('product_value'))
    t_orders_jigawa = CustomerOrders.objects.filter(category_id=id, state='jigawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_kaduna = CustomerOrders.objects.filter(category_id=id, state='kaduna', date_added=today).aggregate(Sum('product_value'))
    t_orders_kano = CustomerOrders.objects.filter(category_id=id, state='kano', date_added=today).aggregate(Sum('product_value'))
    t_orders_katsina = CustomerOrders.objects.filter(category_id=id, state='katsina', date_added=today).aggregate(Sum('product_value'))
    t_orders_kebbi = CustomerOrders.objects.filter(category_id=id, state='kebbi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kogi = CustomerOrders.objects.filter(category_id=id, state='kogi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kwara = CustomerOrders.objects.filter(category_id=id, state='kwara', date_added=today).aggregate(Sum('product_value'))
    t_orders_lagos = CustomerOrders.objects.filter(category_id=id, state='lagos', date_added=today).aggregate(Sum('product_value'))
    t_orders_nasarawa = CustomerOrders.objects.filter(category_id=id, state='nasarawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter(category_id=id, state='niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_ogun = CustomerOrders.objects.filter(category_id=id, state='ogun', date_added=today).aggregate(Sum('product_value'))
    t_orders_ondo = CustomerOrders.objects.filter(category_id=id, state='ondo', date_added=today).aggregate(Sum('product_value'))
    t_orders_osun = CustomerOrders.objects.filter(category_id=id, state='osun', date_added=today).aggregate(Sum('product_value'))
    t_orders_oyo = CustomerOrders.objects.filter(category_id=id, state='oyo', date_added=today).aggregate(Sum('product_value'))
    t_orders_plateau = CustomerOrders.objects.filter(category_id=id, state='plateau', date_added=today).aggregate(Sum('product_value'))
    t_orders_rivers = CustomerOrders.objects.filter(category_id=id, state='rivers', date_added=today).aggregate(Sum('product_value'))
    t_orders_sokoto = CustomerOrders.objects.filter(category_id=id, state='sokoto', date_added=today).aggregate(Sum('product_value'))
    t_orders_taraba = CustomerOrders.objects.filter(category_id=id, state='taraba', date_added=today).aggregate(Sum('product_value'))
    t_orders_yobe = CustomerOrders.objects.filter(category_id=id, state='yobe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zamfara= CustomerOrders.objects.filter(category_id=id, state='zamfara', date_added=today).aggregate(Sum('product_value'))
    t_orders_abuja = CustomerOrders.objects.filter(category_id=id, state='abuja', date_added=today).aggregate(Sum('product_value'))
    t_orders_spain = CustomerOrders.objects.filter(category_id=id, state='spain', date_added=today).aggregate(Sum('product_value'))
    t_orders_usa = CustomerOrders.objects.filter(category_id=id, state='USA', date_added=today).aggregate(Sum('product_value'))
    t_orders_uk = CustomerOrders.objects.filter(category_id=id, state='UK', date_added=today).aggregate(Sum('product_value'))
    t_orders_ghana = CustomerOrders.objects.filter(category_id=id, state='Ghana', date_added=today).aggregate(Sum('product_value'))
    t_orders_canada = CustomerOrders.objects.filter(category_id=id, state='canada', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter(category_id=id, state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter(category_id=id, state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter(category_id=id, state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter(category_id=id, state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_saudi = CustomerOrders.objects.filter(category_id=id, state='Saudi Arabia', date_added=today).aggregate(Sum('product_value'))
    t_orders_south = CustomerOrders.objects.filter(category_id=id, state='South Africa', date_added=today).aggregate(Sum('product_value'))
    t_orders_switzerland = CustomerOrders.objects.filter(category_id=id, state='Switzerland', date_added=today).aggregate(Sum('product_value'))
    t_orders_turkey = CustomerOrders.objects.filter(category_id=id, state='Turkey', date_added=today).aggregate(Sum('product_value'))

    t_orders_zimbabwe = CustomerOrders.objects.filter(category_id=id, state='Zimbabwe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zambia = CustomerOrders.objects.filter(category_id=id, state='Zambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_yemen = CustomerOrders.objects.filter(category_id=id, state='Yemen', date_added=today).aggregate(Sum('product_value'))
    t_orders_venezuela = CustomerOrders.objects.filter(category_id=id, state='Venezuela', date_added=today).aggregate(Sum('product_value'))
    t_orders_uzbekistan = CustomerOrders.objects.filter(category_id=id, state='Uzbekistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_uruguay = CustomerOrders.objects.filter(category_id=id, state='Uruguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_uae = CustomerOrders.objects.filter(category_id=id, state='United Arab Emirates', date_added=today).aggregate(Sum('product_value'))
    t_orders_ukraine = CustomerOrders.objects.filter(category_id=id, state='Ukraine', date_added=today).aggregate(Sum('product_value'))
    t_orders_uganda = CustomerOrders.objects.filter(category_id=id, state='Uganda', date_added=today).aggregate(Sum('product_value'))
    t_orders_tunisia = CustomerOrders.objects.filter(category_id=id, state='Tunisia', date_added=today).aggregate(Sum('product_value'))
    t_orders_trinidad = CustomerOrders.objects.filter(category_id=id, state='Trinidad and Tobago', date_added=today).aggregate(Sum('product_value'))
    t_orders_togo = CustomerOrders.objects.filter(category_id=id, state='Togo', date_added=today).aggregate(Sum('product_value'))
    t_orders_thailand = CustomerOrders.objects.filter(category_id=id, state='Thailand', date_added=today).aggregate(Sum('product_value'))
    t_orders_tanzania = CustomerOrders.objects.filter(category_id=id, state='Tanzania', date_added=today).aggregate(Sum('product_value'))
    t_orders_taiwan = CustomerOrders.objects.filter(category_id=id, state='Taiwan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sweden = CustomerOrders.objects.filter(category_id=id, state='Sweden', date_added=today).aggregate(Sum('product_value'))
    t_orders_swaziland = CustomerOrders.objects.filter(category_id=id, state='Swaziland', date_added=today).aggregate(Sum('product_value'))
    t_orders_sudan = CustomerOrders.objects.filter(category_id=id, state='Sudan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sri = CustomerOrders.objects.filter(category_id=id, state='Sri Lanka', date_added=today).aggregate(Sum('product_value'))
    t_orders_somalia = CustomerOrders.objects.filter(category_id=id, state='Somalia', date_added=today).aggregate(Sum('product_value'))
    t_orders_solomon = CustomerOrders.objects.filter(category_id=id, state='Solomon Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovenia = CustomerOrders.objects.filter(category_id=id, state='Slovenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovakia = CustomerOrders.objects.filter(category_id=id, state='Slovakia', date_added=today).aggregate(Sum('product_value'))
    t_orders_singapore = CustomerOrders.objects.filter(category_id=id, state='Singapore', date_added=today).aggregate(Sum('product_value'))
    t_orders_sierra = CustomerOrders.objects.filter(category_id=id, state='Sierra Leone', date_added=today).aggregate(Sum('product_value'))
    t_orders_serbia = CustomerOrders.objects.filter(category_id=id, state='Serbia', date_added=today).aggregate(Sum('product_value'))
    t_orders_senegal = CustomerOrders.objects.filter(category_id=id, state='Senegal', date_added=today).aggregate(Sum('product_value'))
    t_orders_san = CustomerOrders.objects.filter(category_id=id, state='San Marino', date_added=today).aggregate(Sum('product_value'))
    t_orders_rwanda = CustomerOrders.objects.filter(category_id=id, state='Rwanda', date_added=today).aggregate(Sum('product_value'))
    t_orders_russia = CustomerOrders.objects.filter(category_id=id, state='Russian Federation', date_added=today).aggregate(Sum('product_value'))
    t_orders_romania = CustomerOrders.objects.filter(category_id=id, state='Romania', date_added=today).aggregate(Sum('product_value'))
    t_orders_qatar = CustomerOrders.objects.filter(category_id=id, state='Qatar', date_added=today).aggregate(Sum('product_value'))
    t_orders_portugal = CustomerOrders.objects.filter(category_id=id, state='Portugal', date_added=today).aggregate(Sum('product_value'))
    t_orders_poland = CustomerOrders.objects.filter(category_id=id, state='Poland', date_added=today).aggregate(Sum('product_value'))
    t_orders_philippines = CustomerOrders.objects.filter(category_id=id, state='Philippines', date_added=today).aggregate(Sum('product_value'))
    t_orders_peru = CustomerOrders.objects.filter(category_id=id, state='Peru', date_added=today).aggregate(Sum('product_value'))
    t_orders_paraguay = CustomerOrders.objects.filter(category_id=id, state='Paraguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_pakistan = CustomerOrders.objects.filter(category_id=id, state='Pakistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_oman = CustomerOrders.objects.filter(category_id=id, state='Oman', date_added=today).aggregate(Sum('product_value'))
    t_orders_norway = CustomerOrders.objects.filter(category_id=id, state='Norway', date_added=today).aggregate(Sum('product_value'))
    t_orders_niue = CustomerOrders.objects.filter(category_id=id, state='Niue', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter(category_id=id, state='Niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_nicaragua = CustomerOrders.objects.filter(category_id=id, state='Nicaragua', date_added=today).aggregate(Sum('product_value'))
    t_orders_newz = CustomerOrders.objects.filter(category_id=id, state='New Zealand', date_added=today).aggregate(Sum('product_value'))
    t_orders_netherlands = CustomerOrders.objects.filter(category_id=id, state='Netherlands', date_added=today).aggregate(Sum('product_value'))
    t_orders_nepal = CustomerOrders.objects.filter(category_id=id, state='Nepal', date_added=today).aggregate(Sum('product_value'))
    t_orders_namibia = CustomerOrders.objects.filter(category_id=id, state='Namibia', date_added=today).aggregate(Sum('product_value'))
    t_orders_mozambique = CustomerOrders.objects.filter(category_id=id, state='Mozambique', date_added=today).aggregate(Sum('product_value'))
    t_orders_morocco = CustomerOrders.objects.filter(category_id=id, state='Morocco', date_added=today).aggregate(Sum('product_value'))
    t_orders_montenegro = CustomerOrders.objects.filter(category_id=id, state='Montenegro', date_added=today).aggregate(Sum('product_value'))
    t_orders_mongolia = CustomerOrders.objects.filter(category_id=id, state='Mongolia', date_added=today).aggregate(Sum('product_value'))
    t_orders_moldova = CustomerOrders.objects.filter(category_id=id, state='Moldova', date_added=today).aggregate(Sum('product_value'))
    t_orders_mexico = CustomerOrders.objects.filter(category_id=id, state='Mexico', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritius = CustomerOrders.objects.filter(category_id=id, state='Mauritius', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritania = CustomerOrders.objects.filter(category_id=id, state='Mauritania', date_added=today).aggregate(Sum('product_value'))
    t_orders_malta = CustomerOrders.objects.filter(category_id=id, state='Malta', date_added=today).aggregate(Sum('product_value'))
    t_orders_mali = CustomerOrders.objects.filter(category_id=id, state='Mali', date_added=today).aggregate(Sum('product_value'))
    t_orders_malaysia = CustomerOrders.objects.filter(category_id=id, state='Malaysia', date_added=today).aggregate(Sum('product_value'))
    t_orders_malawi = CustomerOrders.objects.filter(category_id=id, state='Malawi', date_added=today).aggregate(Sum('product_value'))
    t_orders_madagascar = CustomerOrders.objects.filter(category_id=id, state='Madagascar', date_added=today).aggregate(Sum('product_value'))
    t_orders_luxembourg = CustomerOrders.objects.filter(category_id=id, state='Luxembourg', date_added=today).aggregate(Sum('product_value'))
    t_orders_lithuania = CustomerOrders.objects.filter(category_id=id, state='Lithuania', date_added=today).aggregate(Sum('product_value'))
    t_orders_liechtenstein = CustomerOrders.objects.filter(category_id=id, state='Liechtenstein', date_added=today).aggregate(Sum('product_value'))
    t_orders_libya = CustomerOrders.objects.filter(category_id=id, state='Libya', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter(category_id=id, state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_lesotho = CustomerOrders.objects.filter(category_id=id, state='Lesotho', date_added=today).aggregate(Sum('product_value'))
    t_orders_lebanon = CustomerOrders.objects.filter(category_id=id, state='Lebanon', date_added=today).aggregate(Sum('product_value'))
    t_orders_latvia = CustomerOrders.objects.filter(category_id=id, state='Latvia', date_added=today).aggregate(Sum('product_value'))
    t_orders_kuwait = CustomerOrders.objects.filter(category_id=id, state='Kuwait', date_added=today).aggregate(Sum('product_value'))
    t_orders_korea = CustomerOrders.objects.filter(category_id=id, state='Korea', date_added=today).aggregate(Sum('product_value'))
    t_orders_kenya = CustomerOrders.objects.filter(category_id=id, state='Kenya', date_added=today).aggregate(Sum('product_value'))
    t_orders_kazakhstan = CustomerOrders.objects.filter(category_id=id, state='Kazakhstan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jordan = CustomerOrders.objects.filter(category_id=id, state='Jordan', date_added=today).aggregate(Sum('product_value'))
    t_orders_japan = CustomerOrders.objects.filter(category_id=id, state='Japan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jamaica = CustomerOrders.objects.filter(category_id=id, state='Jamaica', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter(category_id=id, state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_israel = CustomerOrders.objects.filter(category_id=id, state='Israel', date_added=today).aggregate(Sum('product_value'))
    t_orders_ireland = CustomerOrders.objects.filter(category_id=id, state='Ireland', date_added=today).aggregate(Sum('product_value'))
    t_orders_iran = CustomerOrders.objects.filter(category_id=id, state='Iran', date_added=today).aggregate(Sum('product_value'))
    t_orders_iraq = CustomerOrders.objects.filter(category_id=id, state='Iraq', date_added=today).aggregate(Sum('product_value'))
    t_orders_indonesia = CustomerOrders.objects.filter(category_id=id, state='Indonesia', date_added=today).aggregate(Sum('product_value'))
    t_orders_india = CustomerOrders.objects.filter(category_id=id, state='India', date_added=today).aggregate(Sum('product_value'))
    t_orders_iceland = CustomerOrders.objects.filter(category_id=id, state='Iceland', date_added=today).aggregate(Sum('product_value'))
    t_orders_hungary = CustomerOrders.objects.filter(category_id=id, state='Hungary', date_added=today).aggregate(Sum('product_value'))
    t_orders_hong = CustomerOrders.objects.filter(category_id=id, state='Hong Kong', date_added=today).aggregate(Sum('product_value'))
    t_orders_honduras = CustomerOrders.objects.filter(category_id=id, state='Honduras', date_added=today).aggregate(Sum('product_value'))
    t_orders_haiti = CustomerOrders.objects.filter(category_id=id, state='Haiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_guineab = CustomerOrders.objects.filter(category_id=id, state='Guinea-Bissau', date_added=today).aggregate(Sum('product_value'))
    t_orders_guinea = CustomerOrders.objects.filter(category_id=id, state='Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_guatemala = CustomerOrders.objects.filter(category_id=id, state='Guatemala', date_added=today).aggregate(Sum('product_value'))
    t_orders_greenland = CustomerOrders.objects.filter(category_id=id, state='Greenland', date_added=today).aggregate(Sum('product_value'))
    t_orders_greece = CustomerOrders.objects.filter(category_id=id, state='Greece', date_added=today).aggregate(Sum('product_value'))
    t_orders_gibraltar = CustomerOrders.objects.filter(category_id=id, state='Gibraltar', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter(category_id=id, state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_georgia = CustomerOrders.objects.filter(category_id=id, state='Georgia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gambia = CustomerOrders.objects.filter(category_id=id, state='Gambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gabon = CustomerOrders.objects.filter(category_id=id, state='Gabon', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter(category_id=id, state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_finland = CustomerOrders.objects.filter(category_id=id, state='Finland', date_added=today).aggregate(Sum('product_value'))
    t_orders_faroe = CustomerOrders.objects.filter(category_id=id, state='Faroe Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_ethiopia = CustomerOrders.objects.filter(category_id=id, state='Ethiopia', date_added=today).aggregate(Sum('product_value'))
    t_orders_estonia = CustomerOrders.objects.filter(category_id=id, state='Estonia', date_added=today).aggregate(Sum('product_value'))
    t_orders_eritrea = CustomerOrders.objects.filter(category_id=id, state='Eritrea', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter(category_id=id, state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_els = CustomerOrders.objects.filter(category_id=id, state='El Salvador', date_added=today).aggregate(Sum('product_value'))
    t_orders_egypt = CustomerOrders.objects.filter(category_id=id, state='Egypt', date_added=today).aggregate(Sum('product_value'))
    t_orders_ecuador = CustomerOrders.objects.filter(category_id=id, state='Ecuador', date_added=today).aggregate(Sum('product_value'))
    t_orders_denmark = CustomerOrders.objects.filter(category_id=id, state='Denmark', date_added=today).aggregate(Sum('product_value'))
    t_orders_czech = CustomerOrders.objects.filter(category_id=id, state='Czech Republic', date_added=today).aggregate(Sum('product_value'))
    t_orders_cyprus = CustomerOrders.objects.filter(category_id=id, state='Cyprus', date_added=today).aggregate(Sum('product_value'))
    t_orders_cuba = CustomerOrders.objects.filter(category_id=id, state='Cuba', date_added=today).aggregate(Sum('product_value'))
    t_orders_croatia = CustomerOrders.objects.filter(category_id=id, state='Croatia', date_added=today).aggregate(Sum('product_value'))
    t_orders_ivory = CustomerOrders.objects.filter(category_id=id, state='Ivory Coast', date_added=today).aggregate(Sum('product_value'))
    t_orders_costa = CustomerOrders.objects.filter(category_id=id, state='Costa Rica', date_added=today).aggregate(Sum('product_value'))
    t_orders_congo = CustomerOrders.objects.filter(category_id=id, state='Congo', date_added=today).aggregate(Sum('product_value'))
    t_orders_colombia = CustomerOrders.objects.filter(category_id=id, state='Colombia', date_added=today).aggregate(Sum('product_value'))
    t_orders_christmas = CustomerOrders.objects.filter(category_id=id, state='Christmas Island', date_added=today).aggregate(Sum('product_value'))
    t_orders_china = CustomerOrders.objects.filter(category_id=id, state='China', date_added=today).aggregate(Sum('product_value'))
    t_orders_chile = CustomerOrders.objects.filter(category_id=id, state='Chile', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter(category_id=id, state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_chad = CustomerOrders.objects.filter(category_id=id, state='Chad', date_added=today).aggregate(Sum('product_value'))
    t_orders_central = CustomerOrders.objects.filter(category_id=id, state='Central African Republi', date_added=today).aggregate(Sum('product_value'))
    t_orders_cape = CustomerOrders.objects.filter(category_id=id, state='Cape Verde', date_added=today).aggregate(Sum('product_value'))
    t_orders_cameroo = CustomerOrders.objects.filter(category_id=id, state='Cameroo', date_added=today).aggregate(Sum('product_value'))
    t_orders_burundi = CustomerOrders.objects.filter(category_id=id, state='Burundi', date_added=today).aggregate(Sum('product_value'))
    t_orders_burkina = CustomerOrders.objects.filter(category_id=id, state='Burkina Faso', date_added=today).aggregate(Sum('product_value'))
    t_orders_bulgaria = CustomerOrders.objects.filter(category_id=id, state='Bulgaria', date_added=today).aggregate(Sum('product_value'))
    t_orders_brazil = CustomerOrders.objects.filter(category_id=id, state='Brazil', date_added=today).aggregate(Sum('product_value'))
    t_orders_botswana = CustomerOrders.objects.filter(category_id=id, state='Botswana', date_added=today).aggregate(Sum('product_value'))
    t_orders_bosnia = CustomerOrders.objects.filter(category_id=id, state='Bosnia and Herzegovina', date_added=today).aggregate(Sum('product_value'))
    t_orders_bolivia = CustomerOrders.objects.filter(category_id=id, state='Bolivia', date_added=today).aggregate(Sum('product_value'))
    t_orders_benin = CustomerOrders.objects.filter(category_id=id, state='Benin', date_added=today).aggregate(Sum('product_value'))
    t_orders_belgium = CustomerOrders.objects.filter(category_id=id, state='Belgium', date_added=today).aggregate(Sum('product_value'))
    t_orders_belarus = CustomerOrders.objects.filter(category_id=id, state='Belarus', date_added=today).aggregate(Sum('product_value'))
    t_orders_barbados = CustomerOrders.objects.filter(category_id=id, state='Barbados', date_added=today).aggregate(Sum('product_value'))
    t_orders_bangladesh = CustomerOrders.objects.filter(category_id=id, state='Bangladesh', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahrain = CustomerOrders.objects.filter(category_id=id, state='Bahrain', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahamas = CustomerOrders.objects.filter(category_id=id, state='Bahamas', date_added=today).aggregate(Sum('product_value'))
    t_orders_azerbaija = CustomerOrders.objects.filter(category_id=id, state='Azerbaija', date_added=today).aggregate(Sum('product_value'))
    t_orders_austria = CustomerOrders.objects.filter(category_id=id, state='Austria', date_added=today).aggregate(Sum('product_value'))
    t_orders_australi = CustomerOrders.objects.filter(category_id=id, state='Australi', date_added=today).aggregate(Sum('product_value'))
    t_orders_armenia = CustomerOrders.objects.filter(category_id=id, state='Armenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_argentina = CustomerOrders.objects.filter(category_id=id, state='Argentina', date_added=today).aggregate(Sum('product_value'))
    t_orders_angola = CustomerOrders.objects.filter(category_id=id, state='Angola', date_added=today).aggregate(Sum('product_value'))
    t_orders_algeria = CustomerOrders.objects.filter(category_id=id, state='Algeria', date_added=today).aggregate(Sum('product_value'))
    t_orders_albania = CustomerOrders.objects.filter(category_id=id, state='Albania', date_added=today).aggregate(Sum('product_value'))
    t_orders_afghanistan = CustomerOrders.objects.filter(category_id=id, state='Afghanistan', date_added=today).aggregate(Sum('product_value'))


    product_value_total_y = CustomerOrders.objects.filter(category_id=id, date_added=yesterday).aggregate(Sum('product_value'))

    y_orders_Jakande = CustomerOrders.objects.filter(category_id=id, state='Jakande', date_added=today).aggregate(Sum('product_value'))
    y_orders_Sangotedo = CustomerOrders.objects.filter(category_id=id, state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    y_orders_Eleko = CustomerOrders.objects.filter(category_id=id, state='Eleko', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ajah = CustomerOrders.objects.filter(category_id=id, state='Ajah', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ogba = CustomerOrders.objects.filter(category_id=id, state='Ogba', date_added=today).aggregate(Sum('product_value'))
    y_orders_Aguda = CustomerOrders.objects.filter(category_id=id, state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ketu = CustomerOrders.objects.filter(category_id=id, state='Ketu', date_added=today).aggregate(Sum('product_value'))
    y_orders_VI = CustomerOrders.objects.filter(category_id=id, state='VI', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikotun = CustomerOrders.objects.filter( category_id=id,state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    y_orders_Oshodi = CustomerOrders.objects.filter(category_id=id, state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikeja = CustomerOrders.objects.filter(category_id=id, state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    y_orders_Lekki = CustomerOrders.objects.filter(category_id=id, state='Lekki', date_added=today).aggregate(Sum('product_value'))
    y_orders_Apapa = CustomerOrders.objects.filter(category_id=id, state='Apapa', date_added=today).aggregate(Sum('product_value'))

    y_orders_abia = CustomerOrders.objects.filter(category_id=id, state='abia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_adamawa = CustomerOrders.objects.filter(category_id=id, state='adamawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_anambra = CustomerOrders.objects.filter(category_id=id, state='anambra', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_akwa_ibom = CustomerOrders.objects.filter(category_id=id, state='akwa-ibom', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bauchi = CustomerOrders.objects.filter(category_id=id, state='bauchi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bayelsa = CustomerOrders.objects.filter(category_id=id, state='bayelsa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benue = CustomerOrders.objects.filter(category_id=id, state='benue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_borno = CustomerOrders.objects.filter(category_id=id, state='borno', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cross_river = CustomerOrders.objects.filter(category_id=id, state='cross-river', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_delta = CustomerOrders.objects.filter(category_id=id, state='delta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ebonyi = CustomerOrders.objects.filter(category_id=id, state='ebonyi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_enugu = CustomerOrders.objects.filter(category_id=id, state='enugu', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_edo = CustomerOrders.objects.filter(category_id=id, state='edo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ekiti = CustomerOrders.objects.filter(category_id=id, state='ekiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gombe = CustomerOrders.objects.filter(category_id=id, state='gombe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_imo = CustomerOrders.objects.filter(category_id=id, state='imo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jigawa = CustomerOrders.objects.filter(category_id=id, state='jigawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kaduna = CustomerOrders.objects.filter(category_id=id, state='kaduna', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kano = CustomerOrders.objects.filter(category_id=id, state='kano', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_katsina = CustomerOrders.objects.filter(category_id=id, state='katsina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kebbi = CustomerOrders.objects.filter(category_id=id, state='kebbi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kogi = CustomerOrders.objects.filter(category_id=id, state='kogi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kwara = CustomerOrders.objects.filter(category_id=id, state='kwara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lagos = CustomerOrders.objects.filter(category_id=id, state='lagos', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nasarawa = CustomerOrders.objects.filter(category_id=id, state='nasarawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter(category_id=id, state='niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ogun = CustomerOrders.objects.filter(category_id=id, state='ogun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ondo = CustomerOrders.objects.filter(category_id=id, state='ondo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_osun = CustomerOrders.objects.filter(category_id=id, state='osun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oyo = CustomerOrders.objects.filter(category_id=id, state='oyo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_plateau = CustomerOrders.objects.filter(category_id=id, state='plateau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rivers = CustomerOrders.objects.filter(category_id=id, state='rivers', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sokoto = CustomerOrders.objects.filter(category_id=id, state='sokoto', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taraba = CustomerOrders.objects.filter(category_id=id, state='taraba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yobe = CustomerOrders.objects.filter(category_id=id, state='yobe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zamfara= CustomerOrders.objects.filter(category_id=id, state='zamfara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_abuja = CustomerOrders.objects.filter(category_id=id, state='abuja', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_spain = CustomerOrders.objects.filter(category_id=id, state='spain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_usa = CustomerOrders.objects.filter(category_id=id, state='USA', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uk = CustomerOrders.objects.filter(category_id=id, state='UK', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ghana = CustomerOrders.objects.filter(category_id=id, state='Ghana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_canada = CustomerOrders.objects.filter(category_id=id, state='canada', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter(category_id=id, state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter(category_id=id, state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter(category_id=id, state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter(category_id=id, state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_saudi = CustomerOrders.objects.filter(category_id=id, state='Saudi Arabia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_south = CustomerOrders.objects.filter(category_id=id, state='South Africa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_switzerland = CustomerOrders.objects.filter(category_id=id, state='Switzerland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_turkey = CustomerOrders.objects.filter(category_id=id, state='Turkey', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zimbabwe = CustomerOrders.objects.filter(category_id=id, state='Zimbabwe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zambia = CustomerOrders.objects.filter(category_id=id, state='Zambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yemen = CustomerOrders.objects.filter(category_id=id, state='Yemen', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_venezuela = CustomerOrders.objects.filter(category_id=id, state='Venezuela', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uzbekistan = CustomerOrders.objects.filter(category_id=id, state='Uzbekistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uruguay = CustomerOrders.objects.filter(category_id=id, state='Uruguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uae = CustomerOrders.objects.filter(category_id=id, state='United Arab Emirates', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ukraine = CustomerOrders.objects.filter(category_id=id, state='Ukraine', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uganda = CustomerOrders.objects.filter(category_id=id, state='Uganda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tunisia = CustomerOrders.objects.filter(category_id=id, state='Tunisia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_trinidad = CustomerOrders.objects.filter(category_id=id, state='Trinidad and Tobago', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_togo = CustomerOrders.objects.filter(category_id=id, state='Togo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_thailand = CustomerOrders.objects.filter(category_id=id, state='Thailand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tanzania = CustomerOrders.objects.filter(category_id=id, state='Tanzania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taiwan = CustomerOrders.objects.filter(category_id=id, state='Taiwan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sweden = CustomerOrders.objects.filter(category_id=id, state='Sweden', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_swaziland = CustomerOrders.objects.filter(category_id=id, state='Swaziland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sudan = CustomerOrders.objects.filter(category_id=id, state='Sudan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sri = CustomerOrders.objects.filter(category_id=id, state='Sri Lanka', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_somalia = CustomerOrders.objects.filter(category_id=id, state='Somalia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_solomon = CustomerOrders.objects.filter(category_id=id, state='Solomon Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovenia = CustomerOrders.objects.filter(category_id=id, state='Slovenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovakia = CustomerOrders.objects.filter(category_id=id, state='Slovakia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_singapore = CustomerOrders.objects.filter(category_id=id, state='Singapore', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sierra = CustomerOrders.objects.filter(category_id=id, state='Sierra Leone', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_serbia = CustomerOrders.objects.filter(category_id=id, state='Serbia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_senegal = CustomerOrders.objects.filter(category_id=id, state='Senegal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_san = CustomerOrders.objects.filter(category_id=id, state='San Marino', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rwanda = CustomerOrders.objects.filter(category_id=id, state='Rwanda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_russia = CustomerOrders.objects.filter(category_id=id, state='Russian Federation', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_romania = CustomerOrders.objects.filter(category_id=id, state='Romania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_qatar = CustomerOrders.objects.filter(category_id=id, state='Qatar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_portugal = CustomerOrders.objects.filter(category_id=id, state='Portugal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_poland = CustomerOrders.objects.filter(category_id=id, state='Poland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_philippines = CustomerOrders.objects.filter(category_id=id, state='Philippines', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_peru = CustomerOrders.objects.filter(category_id=id, state='Peru', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_paraguay = CustomerOrders.objects.filter(category_id=id, state='Paraguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_pakistan = CustomerOrders.objects.filter(category_id=id, state='Pakistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oman = CustomerOrders.objects.filter(category_id=id, state='Oman', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_norway = CustomerOrders.objects.filter(category_id=id, state='Norway', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niue = CustomerOrders.objects.filter(category_id=id, state='Niue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter(category_id=id, state='Niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nicaragua = CustomerOrders.objects.filter(category_id=id, state='Nicaragua', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_newz = CustomerOrders.objects.filter(category_id=id, state='New Zealand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_netherlands = CustomerOrders.objects.filter(category_id=id, state='Netherlands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nepal = CustomerOrders.objects.filter(category_id=id, state='Nepal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_namibia = CustomerOrders.objects.filter(category_id=id, state='Namibia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mozambique = CustomerOrders.objects.filter(category_id=id, state='Mozambique', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_morocco = CustomerOrders.objects.filter(category_id=id, state='Morocco', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_montenegro = CustomerOrders.objects.filter(category_id=id, state='Montenegro', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mongolia = CustomerOrders.objects.filter(category_id=id, state='Mongolia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_moldova = CustomerOrders.objects.filter(category_id=id, state='Moldova', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mexico = CustomerOrders.objects.filter(category_id=id, state='Mexico', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritius = CustomerOrders.objects.filter(category_id=id, state='Mauritius', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritania = CustomerOrders.objects.filter(category_id=id, state='Mauritania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malta = CustomerOrders.objects.filter(category_id=id, state='Malta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mali = CustomerOrders.objects.filter(category_id=id, state='Mali', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malaysia = CustomerOrders.objects.filter(category_id=id, state='Malaysia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malawi = CustomerOrders.objects.filter(category_id=id, state='Malawi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_madagascar = CustomerOrders.objects.filter(category_id=id, state='Madagascar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_luxembourg = CustomerOrders.objects.filter(category_id=id, state='Luxembourg', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lithuania = CustomerOrders.objects.filter(category_id=id, state='Lithuania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liechtenstein = CustomerOrders.objects.filter(category_id=id, state='Liechtenstein', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_libya = CustomerOrders.objects.filter(category_id=id, state='Libya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter(category_id=id, state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lesotho = CustomerOrders.objects.filter(category_id=id, state='Lesotho', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lebanon = CustomerOrders.objects.filter(category_id=id, state='Lebanon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_latvia = CustomerOrders.objects.filter(category_id=id, state='Latvia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kuwait = CustomerOrders.objects.filter(category_id=id, state='Kuwait', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_korea = CustomerOrders.objects.filter(category_id=id, state='Korea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kenya = CustomerOrders.objects.filter(category_id=id, state='Kenya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kazakhstan = CustomerOrders.objects.filter(category_id=id, state='Kazakhstan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jordan = CustomerOrders.objects.filter(category_id=id, state='Jordan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_japan = CustomerOrders.objects.filter(category_id=id, state='Japan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jamaica = CustomerOrders.objects.filter(category_id=id, state='Jamaica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter(category_id=id, state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_israel = CustomerOrders.objects.filter(category_id=id, state='Israel', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ireland = CustomerOrders.objects.filter(category_id=id, state='Ireland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iran = CustomerOrders.objects.filter(category_id=id, state='Iran', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iraq = CustomerOrders.objects.filter(category_id=id, state='Iraq', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_indonesia = CustomerOrders.objects.filter(category_id=id, state='Indonesia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_india = CustomerOrders.objects.filter(category_id=id, state='India', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iceland = CustomerOrders.objects.filter(category_id=id, state='Iceland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hungary = CustomerOrders.objects.filter(category_id=id, state='Hungary', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hong = CustomerOrders.objects.filter(category_id=id, state='Hong Kong', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_honduras = CustomerOrders.objects.filter(category_id=id, state='Honduras', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_haiti = CustomerOrders.objects.filter(category_id=id, state='Haiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guineab = CustomerOrders.objects.filter(category_id=id, state='Guinea-Bissau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guinea = CustomerOrders.objects.filter(category_id=id, state='Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guatemala = CustomerOrders.objects.filter(category_id=id, state='Guatemala', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greenland = CustomerOrders.objects.filter(category_id=id, state='Greenland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greece = CustomerOrders.objects.filter(category_id=id, state='Greece', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gibraltar = CustomerOrders.objects.filter(category_id=id, state='Gibraltar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter(category_id=id, state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_georgia = CustomerOrders.objects.filter(category_id=id, state='Georgia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gambia = CustomerOrders.objects.filter(category_id=id, state='Gambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gabon = CustomerOrders.objects.filter(category_id=id, state='Gabon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter(category_id=id, state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_finland = CustomerOrders.objects.filter(category_id=id, state='Finland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_faroe = CustomerOrders.objects.filter(category_id=id, state='Faroe Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ethiopia = CustomerOrders.objects.filter(category_id=id, state='Ethiopia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_estonia = CustomerOrders.objects.filter(category_id=id, state='Estonia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_eritrea = CustomerOrders.objects.filter(category_id=id, state='Eritrea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter(category_id=id, state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_els = CustomerOrders.objects.filter(category_id=id, state='El Salvador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_egypt = CustomerOrders.objects.filter(category_id=id, state='Egypt', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ecuador = CustomerOrders.objects.filter(category_id=id, state='Ecuador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_denmark = CustomerOrders.objects.filter(category_id=id, state='Denmark', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_czech = CustomerOrders.objects.filter(category_id=id, state='Czech Republic', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cyprus = CustomerOrders.objects.filter(category_id=id, state='Cyprus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cuba = CustomerOrders.objects.filter(category_id=id, state='Cuba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_croatia = CustomerOrders.objects.filter(category_id=id, state='Croatia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ivory = CustomerOrders.objects.filter(category_id=id, state='Ivory Coast', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_costa = CustomerOrders.objects.filter(category_id=id, state='Costa Rica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_congo = CustomerOrders.objects.filter(category_id=id, state='Congo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_colombia = CustomerOrders.objects.filter(category_id=id, state='Colombia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_christmas = CustomerOrders.objects.filter(category_id=id, state='Christmas Island', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_china = CustomerOrders.objects.filter(category_id=id, state='China', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chile = CustomerOrders.objects.filter(category_id=id, state='Chile', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter(category_id=id, state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chad = CustomerOrders.objects.filter(category_id=id, state='Chad', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_central = CustomerOrders.objects.filter(category_id=id, state='Central African Republi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cape = CustomerOrders.objects.filter(category_id=id, state='Cape Verde', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cameroo = CustomerOrders.objects.filter(category_id=id, state='Cameroo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burundi = CustomerOrders.objects.filter(category_id=id, state='Burundi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burkina = CustomerOrders.objects.filter(category_id=id, state='Burkina Faso', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bulgaria = CustomerOrders.objects.filter(category_id=id, state='Bulgaria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_brazil = CustomerOrders.objects.filter(category_id=id, state='Brazil', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_botswana = CustomerOrders.objects.filter(category_id=id, state='Botswana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bosnia = CustomerOrders.objects.filter(category_id=id, state='Bosnia and Herzegovina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bolivia = CustomerOrders.objects.filter(category_id=id, state='Bolivia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benin = CustomerOrders.objects.filter(category_id=id, state='Benin', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belgium = CustomerOrders.objects.filter(category_id=id, state='Belgium', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belarus = CustomerOrders.objects.filter(category_id=id, state='Belarus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_barbados = CustomerOrders.objects.filter(category_id=id, state='Barbados', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bangladesh = CustomerOrders.objects.filter(category_id=id, state='Bangladesh', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahrain = CustomerOrders.objects.filter(category_id=id, state='Bahrain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahamas = CustomerOrders.objects.filter(category_id=id, state='Bahamas', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_azerbaija = CustomerOrders.objects.filter(category_id=id, state='Azerbaija', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_austria = CustomerOrders.objects.filter(category_id=id, state='Austria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_australi = CustomerOrders.objects.filter(category_id=id, state='Australi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_armenia = CustomerOrders.objects.filter(category_id=id, state='Armenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_argentina = CustomerOrders.objects.filter(category_id=id, state='Argentina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_angola = CustomerOrders.objects.filter(category_id=id, state='Angola', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_algeria = CustomerOrders.objects.filter(category_id=id, state='Algeria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_albania = CustomerOrders.objects.filter(category_id=id, state='Albania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_afghanistan = CustomerOrders.objects.filter(category_id=id, state='Afghanistan', date_added=yesterday).aggregate(Sum('product_value'))


    return render(request, 'inventory/daily_orders.html', {'categories': categories,
                                                            't_orders_Jakande' :  t_orders_Jakande,
                                                            't_orders_Sangotedo': t_orders_Sangotedo,
                                                            't_orders_Eleko': t_orders_Eleko,
                                                            't_orders_Ajah': t_orders_Ajah,
                                                            't_orders_Ogba': t_orders_Ogba,
                                                            't_orders_Aguda': t_orders_Aguda,
                                                            't_orders_Ketu': t_orders_Ketu,
                                                            't_orders_VI': t_orders_VI,
                                                            't_orders_Ikotun': t_orders_Ikotun,
                                                            't_orders_Oshodi': t_orders_Oshodi,
                                                            't_orders_Ikeja': t_orders_Ikeja,
                                                            't_orders_Lekki': t_orders_Lekki ,
                                                            't_orders_Apapa': t_orders_Apapa,

                                                            't_orders_abia': t_orders_abia,
                                                            't_orders_adamawa': t_orders_adamawa,
                                                            't_orders_anambra': t_orders_anambra,
                                                            't_orders_akwa_ibom': t_orders_akwa_ibom,
                                                            't_orders_bauchi': t_orders_bauchi,
                                                            't_orders_bayelsa': t_orders_bayelsa,
                                                            't_orders_benue': t_orders_benue,
                                                            't_orders_borno': t_orders_borno,
                                                            't_orders_cross_river': t_orders_cross_river,
                                                            't_orders_delta': t_orders_delta,
                                                            't_orders_ebonyi': t_orders_ebonyi,
                                                            't_orders_enugu': t_orders_enugu,
                                                            't_orders_edo': t_orders_edo,
                                                            't_orders_ekiti': t_orders_ekiti,
                                                            't_orders_gombe': t_orders_gombe,
                                                            't_orders_imo': t_orders_imo,
                                                            't_orders_jigawa': t_orders_jigawa,
                                                            't_orders_kaduna': t_orders_kaduna,
                                                            't_orders_kano': t_orders_kano,
                                                            't_orders_katsina': t_orders_katsina,
                                                            't_orders_kebbi': t_orders_kebbi,
                                                            't_orders_kogi': t_orders_kogi,
                                                            't_orders_kwara': t_orders_kwara,
                                                            't_orders_lagos': t_orders_lagos,
                                                            't_orders_nasarawa': t_orders_nasarawa,
                                                            't_orders_niger': t_orders_niger,
                                                            't_orders_ogun': t_orders_ogun,
                                                            't_orders_ondo': t_orders_ondo,
                                                            't_orders_osun': t_orders_osun,
                                                            't_orders_oyo': t_orders_oyo,
                                                            't_orders_plateau': t_orders_plateau,
                                                            't_orders_rivers': t_orders_rivers,
                                                            't_orders_sokoto': t_orders_sokoto,
                                                            't_orders_taraba': t_orders_taraba,
                                                            't_orders_yobe': t_orders_yobe,
                                                            't_orders_zamfara': t_orders_zamfara,
                                                            't_orders_abuja': t_orders_abuja,
                                                            't_orders_spain': t_orders_spain,
                                                            't_orders_usa': t_orders_usa,
                                                            't_orders_uk': t_orders_uk,
                                                            't_orders_ghana': t_orders_ghana,
                                                            't_orders_canada': t_orders_canada,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_saudi': t_orders_saudi,
                                                            't_orders_south': t_orders_south,
                                                            't_orders_switzerland': t_orders_switzerland,
                                                            't_orders_turkey': t_orders_turkey,

                                                            't_orders_zimbabwe' : t_orders_zimbabwe,
                                                            't_orders_zambia':  t_orders_zambia,
                                                            't_orders_yemen': t_orders_yemen,
                                                            't_orders_venezuela': t_orders_venezuela,
                                                            't_orders_uzbekistan': t_orders_uzbekistan,
                                                            't_orders_uruguay': t_orders_uruguay,
                                                            't_orders_uae': t_orders_uae,
                                                            't_orders_ukraine': t_orders_ukraine,
                                                            't_orders_uganda': t_orders_uganda,
                                                            't_orders_tunisia': t_orders_tunisia,
                                                            't_orders_trinidad': t_orders_trinidad,
                                                            't_orders_togo': t_orders_togo,
                                                            't_orders_thailand': t_orders_thailand,
                                                            't_orders_tanzania': t_orders_tanzania,
                                                            't_orders_taiwan': t_orders_taiwan,
                                                            't_orders_sweden': t_orders_sweden,
                                                            't_orders_swaziland': t_orders_swaziland,
                                                            't_orders_sudan': t_orders_sudan,
                                                            't_orders_sri': t_orders_sri,
                                                            't_orders_somalia': t_orders_somalia,
                                                            't_orders_solomon': t_orders_solomon,
                                                            't_orders_slovenia': t_orders_slovenia,
                                                            't_orders_slovakia': t_orders_slovakia,
                                                            't_orders_singapore': t_orders_singapore,
                                                            't_orders_sierra': t_orders_sierra,
                                                            't_orders_serbia': t_orders_serbia,
                                                            't_orders_senegal': t_orders_senegal,
                                                            't_orders_san': t_orders_san,
                                                            't_orders_rwanda': t_orders_rwanda,
                                                            't_orders_russia': t_orders_russia,
                                                            't_orders_romania': t_orders_romania,
                                                            't_orders_qatar': t_orders_qatar,
                                                            't_orders_portugal': t_orders_portugal,
                                                            't_orders_poland': t_orders_poland,
                                                            't_orders_philippines': t_orders_philippines,
                                                            't_orders_peru': t_orders_peru,
                                                            't_orders_paraguay': t_orders_paraguay,
                                                            't_orders_pakistan': t_orders_pakistan,
                                                            't_orders_oman': t_orders_oman,
                                                            't_orders_norway': t_orders_norway,
                                                            't_orders_niue': t_orders_niue,
                                                            't_orders_niger':  t_orders_niger,
                                                            't_orders_nicaragua': t_orders_nicaragua,
                                                            't_orders_newz': t_orders_newz,
                                                            't_orders_netherlands': t_orders_netherlands,
                                                            't_orders_nepal': t_orders_nepal,
                                                            't_orders_namibia': t_orders_namibia,
                                                            't_orders_mozambique': t_orders_mozambique,
                                                            't_orders_morocco': t_orders_morocco,
                                                            't_orders_montenegro': t_orders_montenegro,
                                                            't_orders_mongolia': t_orders_mongolia,
                                                            't_orders_moldova': t_orders_moldova,
                                                            't_orders_mexico': t_orders_mexico,
                                                            't_orders_mauritius': t_orders_mauritius,
                                                            't_orders_mauritania': t_orders_mauritania,
                                                            't_orders_malta': t_orders_malta,
                                                            't_orders_mali': t_orders_mali,
                                                            't_orders_malaysia': t_orders_malaysia,
                                                            't_orders_malawi': t_orders_malawi,
                                                            't_orders_madagascar': t_orders_madagascar,
                                                            't_orders_luxembourg': t_orders_luxembourg,
                                                            't_orders_lithuania': t_orders_lithuania,
                                                            't_orders_liechtenstein': t_orders_liechtenstein,
                                                            't_orders_libya': t_orders_libya,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_lesotho': t_orders_lesotho,
                                                            't_orders_lebanon': t_orders_lebanon,
                                                            't_orders_latvia': t_orders_latvia,
                                                            't_orders_kuwait': t_orders_kuwait,
                                                            't_orders_korea': t_orders_korea,
                                                            't_orders_kenya': t_orders_kenya,
                                                            't_orders_kazakhstan': t_orders_kazakhstan,
                                                            't_orders_jordan': t_orders_jordan,
                                                            't_orders_japan': t_orders_japan,
                                                            't_orders_jamaica': t_orders_jamaica,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_israel': t_orders_israel,
                                                            't_orders_ireland': t_orders_ireland,
                                                            't_orders_iran': t_orders_iran,
                                                            't_orders_iraq': t_orders_iraq,
                                                            't_orders_indonesia': t_orders_indonesia,
                                                            't_orders_india': t_orders_india,
                                                            't_orders_iceland': t_orders_iceland,
                                                            't_orders_hungary': t_orders_hungary,
                                                            't_orders_hong': t_orders_hong,
                                                            't_orders_honduras': t_orders_honduras,
                                                            't_orders_haiti': t_orders_haiti,
                                                            't_orders_guineab': t_orders_guineab,
                                                            't_orders_guinea': t_orders_guinea,
                                                            't_orders_guatemala': t_orders_guatemala,
                                                            't_orders_greenland': t_orders_greenland,
                                                            't_orders_greece': t_orders_greece,
                                                            't_orders_gibraltar': t_orders_gibraltar,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_georgia': t_orders_georgia,
                                                            't_orders_gambia': t_orders_gambia,
                                                            't_orders_gabon': t_orders_gabon,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_finland': t_orders_finland,
                                                            't_orders_faroe': t_orders_faroe,
                                                            't_orders_ethiopia': t_orders_ethiopia,
                                                            't_orders_estonia': t_orders_estonia,
                                                            't_orders_eritrea': t_orders_eritrea,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_els': t_orders_els,
                                                            't_orders_egypt': t_orders_egypt,
                                                            't_orders_ecuador': t_orders_ecuador,
                                                            't_orders_denmark': t_orders_denmark,
                                                            't_orders_czech': t_orders_czech,
                                                            't_orders_cyprus': t_orders_cyprus,
                                                            't_orders_cuba': t_orders_cuba,
                                                            't_orders_croatia': t_orders_croatia,
                                                            't_orders_ivory': t_orders_ivory,
                                                            't_orders_costa': t_orders_costa,
                                                            't_orders_congo': t_orders_congo,
                                                            't_orders_colombia': t_orders_colombia,
                                                            't_orders_christmas': t_orders_christmas,
                                                            't_orders_china': t_orders_china,
                                                            't_orders_chile': t_orders_chile,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_chad': t_orders_chad,
                                                            't_orders_central': t_orders_central,
                                                            't_orders_cape': t_orders_cape,
                                                            't_orders_cameroo': t_orders_cameroo,
                                                            't_orders_burundi': t_orders_burundi,
                                                            't_orders_burkina': t_orders_burkina,
                                                            't_orders_bulgaria': t_orders_bulgaria,
                                                            't_orders_brazil': t_orders_brazil,
                                                            't_orders_botswana': t_orders_botswana,
                                                            't_orders_bosnia': t_orders_bosnia,
                                                            't_orders_bolivia': t_orders_bolivia,
                                                            't_orders_benin': t_orders_benin,
                                                            't_orders_belgium': t_orders_belgium,
                                                            't_orders_belarus': t_orders_belarus,
                                                            't_orders_barbados': t_orders_barbados,
                                                            't_orders_bangladesh': t_orders_bangladesh,
                                                            't_orders_bahrain': t_orders_bahrain,
                                                            't_orders_bahamas': t_orders_bahamas,
                                                            't_orders_azerbaija': t_orders_azerbaija,
                                                            't_orders_austria': t_orders_austria,
                                                            't_orders_australi': t_orders_australi,
                                                            't_orders_armenia': t_orders_armenia,
                                                            't_orders_argentina': t_orders_argentina,
                                                            't_orders_angola': t_orders_angola,
                                                            't_orders_algeria': t_orders_algeria,
                                                            't_orders_albania': t_orders_albania,
                                                            't_orders_afghanistan': t_orders_afghanistan,
                                                            'y_orders_zimbabwe' : y_orders_zimbabwe,
                                                            'y_orders_zambia':  y_orders_zambia,
                                                            'y_orders_yemen': y_orders_yemen,
                                                            'y_orders_venezuela': y_orders_venezuela,
                                                            'y_orders_uzbekistan': y_orders_uzbekistan,
                                                            'y_orders_uruguay': y_orders_uruguay,
                                                            'y_orders_uae': y_orders_uae,
                                                            'y_orders_ukraine': y_orders_ukraine,
                                                            'y_orders_uganda': y_orders_uganda,
                                                            'y_orders_tunisia': y_orders_tunisia,
                                                            'y_orders_trinidad': y_orders_trinidad,
                                                            'y_orders_togo': y_orders_togo,
                                                            'y_orders_thailand': y_orders_thailand,
                                                            'y_orders_tanzania': y_orders_tanzania,
                                                            'y_orders_taiwan': y_orders_taiwan,
                                                            'y_orders_sweden': y_orders_sweden,
                                                            'y_orders_swaziland': y_orders_swaziland,
                                                            'y_orders_sudan': y_orders_sudan,
                                                            'y_orders_sri': y_orders_sri,
                                                            'y_orders_somalia': y_orders_somalia ,
                                                            'y_orders_solomon': y_orders_solomon,
                                                            'y_orders_slovenia': y_orders_slovenia,
                                                            'y_orders_slovakia': y_orders_slovakia,
                                                            'y_orders_singapore': y_orders_singapore,
                                                            'y_orders_sierra': y_orders_sierra,
                                                            'y_orders_serbia': y_orders_serbia,
                                                            'y_orders_senegal': y_orders_senegal,
                                                            'y_orders_san': y_orders_san,
                                                            'y_orders_rwanda': y_orders_rwanda,
                                                            'y_orders_russia': y_orders_russia,
                                                            'y_orders_romania': y_orders_romania,
                                                            'y_orders_qatar': y_orders_qatar,
                                                            'y_orders_portugal': y_orders_portugal,
                                                            'y_orders_poland': y_orders_poland,
                                                            'y_orders_philippines': y_orders_philippines,
                                                            'y_orders_peru': y_orders_peru,
                                                            'y_orders_paraguay': y_orders_paraguay,
                                                            'y_orders_pakistan': y_orders_pakistan,
                                                            'y_orders_oman': y_orders_oman,
                                                            'y_orders_norway': y_orders_norway,
                                                            'y_orders_niue': y_orders_niue,
                                                            'y_orders_niger':  y_orders_niger,
                                                            'y_orders_nicaragua': y_orders_nicaragua,
                                                            'y_orders_newz': y_orders_newz,
                                                            'y_orders_netherlands': y_orders_netherlands,
                                                            'y_orders_nepal': y_orders_nepal,
                                                            'y_orders_namibia': y_orders_namibia,
                                                            'y_orders_mozambique': y_orders_mozambique,
                                                            'y_orders_morocco': y_orders_morocco,
                                                            'y_orders_montenegro': y_orders_montenegro,
                                                            'y_orders_mongolia': y_orders_mongolia,
                                                            'y_orders_moldova': y_orders_moldova,
                                                            'y_orders_mexico': y_orders_mexico,
                                                            'y_orders_mauritius': y_orders_mauritius,
                                                            'y_orders_mauritania': y_orders_mauritania,
                                                            'y_orders_malta': y_orders_malta,
                                                            'y_orders_mali': y_orders_mali,
                                                            'y_orders_malaysia': y_orders_malaysia,
                                                            'y_orders_malawi': y_orders_malawi,
                                                            'y_orders_madagascar': y_orders_madagascar,
                                                            'y_orders_luxembourg': y_orders_luxembourg,
                                                            'y_orders_lithuania': y_orders_lithuania,
                                                            'y_orders_liechtenstein': y_orders_liechtenstein,
                                                            'y_orders_libya': y_orders_libya,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_lesotho': y_orders_lesotho,
                                                            'y_orders_lebanon': y_orders_lebanon,
                                                            'y_orders_latvia': y_orders_latvia,
                                                            'y_orders_kuwait': y_orders_kuwait,
                                                            'y_orders_korea': y_orders_korea,
                                                            'y_orders_kenya': y_orders_kenya,
                                                            'y_orders_kazakhstan': y_orders_kazakhstan,
                                                            'y_orders_jordan': y_orders_jordan,
                                                            'y_orders_japan': y_orders_japan,
                                                            'y_orders_jamaica': y_orders_jamaica,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_israel': y_orders_israel,
                                                            'y_orders_ireland': y_orders_ireland,
                                                            'y_orders_iran': y_orders_iran,
                                                            'y_orders_iraq': y_orders_iraq,
                                                            'y_orders_indonesia': y_orders_indonesia,
                                                            'y_orders_india': y_orders_india,
                                                            'y_orders_iceland': y_orders_iceland,
                                                            'y_orders_hungary': y_orders_hungary,
                                                            'y_orders_hong': y_orders_hong,
                                                            'y_orders_honduras': y_orders_honduras,
                                                            'y_orders_haiti': y_orders_haiti,
                                                            'y_orders_guineab': y_orders_guineab,
                                                            'y_orders_guinea': y_orders_guinea,
                                                            'y_orders_guatemala': y_orders_guatemala,
                                                            'y_orders_greenland': y_orders_greenland,
                                                            'y_orders_greece': y_orders_greece,
                                                            'y_orders_gibraltar': y_orders_gibraltar,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_georgia': y_orders_georgia,
                                                            'y_orders_gambia': y_orders_gambia,
                                                            'y_orders_gabon': y_orders_gabon,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_finland': y_orders_finland,
                                                            'y_orders_faroe': y_orders_faroe,
                                                            'y_orders_ethiopia': y_orders_ethiopia,
                                                            'y_orders_estonia': y_orders_estonia,
                                                            'y_orders_eritrea': y_orders_eritrea,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_els': y_orders_els,
                                                            'y_orders_egypt': y_orders_egypt,
                                                            'y_orders_ecuador': y_orders_ecuador,
                                                            'y_orders_denmark': y_orders_denmark,
                                                            'y_orders_czech': y_orders_czech,
                                                            'y_orders_cyprus': y_orders_cyprus,
                                                            'y_orders_cuba': y_orders_cuba,
                                                            'y_orders_croatia': y_orders_croatia,
                                                            'y_orders_ivory': y_orders_ivory,
                                                            'y_orders_costa': y_orders_costa,
                                                            'y_orders_congo': y_orders_congo,
                                                            'y_orders_colombia': y_orders_colombia,
                                                            'y_orders_christmas': y_orders_christmas,
                                                            'y_orders_china': y_orders_china,
                                                            'y_orders_chile': y_orders_chile,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_chad': y_orders_chad,
                                                            'y_orders_central': y_orders_central,
                                                            'y_orders_cape': y_orders_cape,
                                                            'y_orders_cameroo': y_orders_cameroo,
                                                            'y_orders_burundi': y_orders_burundi,
                                                            'y_orders_burkina': y_orders_burkina,
                                                            'y_orders_bulgaria': y_orders_bulgaria,
                                                            'y_orders_brazil': y_orders_brazil,
                                                            'y_orders_botswana': y_orders_botswana,
                                                            'y_orders_bosnia': y_orders_bosnia,
                                                            'y_orders_bolivia': y_orders_bolivia,
                                                            'y_orders_benin': y_orders_benin,
                                                            'y_orders_belgium': y_orders_belgium,
                                                            'y_orders_belarus': y_orders_belarus,
                                                            'y_orders_barbados': y_orders_barbados,
                                                            'y_orders_bangladesh': y_orders_bangladesh,
                                                            'y_orders_bahrain': y_orders_bahrain,
                                                            'y_orders_bahamas': y_orders_bahamas,
                                                            'y_orders_azerbaija': y_orders_azerbaija,
                                                            'y_orders_austria': y_orders_austria,
                                                            'y_orders_australi': y_orders_australi,
                                                            'y_orders_armenia': y_orders_armenia,
                                                            'y_orders_argentina': y_orders_argentina,
                                                            'y_orders_angola': y_orders_angola,
                                                            'y_orders_algeria': y_orders_algeria,
                                                            'y_orders_albania': y_orders_albania,
                                                            'y_orders_afghanistan': y_orders_afghanistan,
                                                            'is_entry': is_entry,
                                                            'is_lagos': is_lagos,
                                                            'is_daily': is_daily,
                                                            'product_value_total': product_value_total,

                                                            'y_orders_Jakande' :  y_orders_Jakande,
                                                            'y_orders_Sangotedo': y_orders_Sangotedo,
                                                            'y_orders_Eleko': y_orders_Eleko,
                                                            'y_orders_Ajah': y_orders_Ajah,
                                                            'y_orders_Ogba': y_orders_Ogba,
                                                            'y_orders_Aguda': y_orders_Aguda,
                                                            'y_orders_Ketu': y_orders_Ketu,
                                                            'y_orders_VI': y_orders_VI,
                                                            'y_orders_Ikotun': y_orders_Ikotun,
                                                            'y_orders_Oshodi': y_orders_Oshodi,
                                                            'y_orders_Ikeja': y_orders_Ikeja,
                                                            'y_orders_Lekki': y_orders_Lekki ,
                                                            'y_orders_Apapa': y_orders_Apapa,

                                                            'y_orders_abia': y_orders_abia,
                                                            'y_orders_adamawa': y_orders_adamawa,
                                                            'y_orders_anambra': y_orders_anambra,
                                                            'y_orders_akwa_ibom': y_orders_akwa_ibom,
                                                            'y_orders_bauchi': y_orders_bauchi,
                                                            'y_orders_bayelsa': y_orders_bayelsa,
                                                            'y_orders_benue': y_orders_benue,
                                                            'y_orders_borno': y_orders_borno,
                                                            'y_orders_cross_river': y_orders_cross_river,
                                                            'y_orders_delta': y_orders_delta,
                                                            'y_orders_ebonyi': y_orders_ebonyi,
                                                            'y_orders_enugu': y_orders_enugu,
                                                            'y_orders_edo': y_orders_edo,
                                                            'y_orders_ekiti': y_orders_ekiti,
                                                            'y_orders_gombe': y_orders_gombe,
                                                            'y_orders_imo': y_orders_imo,
                                                            'y_orders_jigawa': y_orders_jigawa,
                                                            'y_orders_kaduna': y_orders_kaduna,
                                                            'y_orders_kano': y_orders_kano,
                                                            'y_orders_katsina': y_orders_katsina,
                                                            'y_orders_kebbi': y_orders_kebbi,
                                                            'y_orders_kogi': y_orders_kogi,
                                                            'y_orders_kwara': y_orders_kwara,
                                                            'y_orders_lagos': y_orders_lagos,
                                                            'y_orders_nasarawa': y_orders_nasarawa,
                                                            'y_orders_niger': y_orders_niger,
                                                            'y_orders_ogun': y_orders_ogun,
                                                            'y_orders_ondo': y_orders_ondo,
                                                            'y_orders_osun': y_orders_osun,
                                                            'y_orders_oyo': y_orders_oyo,
                                                            'y_orders_plateau': y_orders_plateau,
                                                            'y_orders_rivers': y_orders_rivers,
                                                            'y_orders_sokoto': y_orders_sokoto,
                                                            'y_orders_taraba': y_orders_taraba,
                                                            'y_orders_yobe': y_orders_yobe,
                                                            'y_orders_zamfara': y_orders_zamfara,
                                                            'y_orders_abuja': y_orders_abuja,
                                                            'y_orders_spain': y_orders_spain,
                                                            'y_orders_usa': y_orders_usa,
                                                            'y_orders_uk': y_orders_uk,
                                                            'y_orders_ghana': y_orders_ghana,
                                                            'y_orders_canada': y_orders_canada,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_saudi': y_orders_saudi,
                                                            'y_orders_south': y_orders_south,
                                                            'y_orders_switzerland': y_orders_switzerland,
                                                            'y_orders_turkey': y_orders_turkey,
                                                            'product_value_total_y': product_value_total_y,
                                                            'category': category,})



@login_required
def today_orders(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    t_orders = CustomerOrders.objects.filter(category_id=id, date_added=today).order_by('-date', '-time')
    paginator = Paginator(t_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': t_orders, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})


@login_required
def today_orders_coms(request, user):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    t_orders = CustomerOrders.objects.filter(date_added=today, coms_exec=user).order_by('-date', '-time')
    paginator = Paginator(t_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': t_orders, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})



@login_required
def yesterday_orders(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    t_orders = CustomerOrders.objects.filter(category_id=id, date_added=yesterday).order_by('-date', '-time')
    paginator = Paginator(t_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': t_orders, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})


@login_required
def yesterday_orders_coms(request, user):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    t_orders = CustomerOrders.objects.filter(date_added=yesterday, coms_exec=user).order_by('-date', '-time')
    paginator = Paginator(t_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': t_orders, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})


@login_required
def coms_exec_orders(request):
    is_comsexec = request.user.groups.filter(name='comsexec').exists()
    coms_orders = CustomerOrders.objects.filter(coms_exec=request.user.username).order_by('-date', '-time')
    paginator = Paginator(coms_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': coms_orders, 'orderss': orderss, 'is_comsexec': is_comsexec})



@login_required
def delete_customer_order(request, id, category):
    CustomerOrders.objects.get(id=id).delete()
    next = request.GET.get('next')
    messages.success(request, category + ' Customer Order Deleted Successfully')
    return redirect(next)



@login_required
def order_status(request, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    categories = Category.objects.all()
    coms_reps = ComsReps.objects.all()
    #cat = Category.objects.get(name=category)
    edit_order = CustomerOrders.objects.get(id=id)
    my_form = OrderStatusForm()
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=edit_order)
        if form.is_valid():
            form.save()
            form = OrderStatusForm(instance=edit_order)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Form')
    else:
        form = OrderStatusForm(instance=edit_order)
    return render(request, 'inventory/order_status.html', {
        'form': form, 'categories': categories, 'coms_reps': coms_reps, 'is_entry': is_entry, 'is_orderstatus': is_orderstatus
    })


@login_required
def delivered_orders(request, category, id):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    categories = Category.objects.all()
    if 'start_date' in request.GET:
            s_date = request.GET['start_date']
            e_date = request.GET['end_date']
            all_orders = CustomerOrders.objects.all().filter(date__range=[s_date, e_date], category_id=id, order_status="DELIVERED").order_by('date', 'time').exclude(amount_paid=0, state="lagos")
    else:
        s_date = None
        e_date = None
        all_orders = CustomerOrders.objects.all().filter(category_id=id, order_status="DELIVERED").order_by('date', 'time').exclude(state="lagos")
    #all_orders = CustomerOrders.objects.filter(category_id=id, order_status="DELIVERED" ).exclude(amount_paid=0).order_by('-date', '-time')
    paginator = Paginator(all_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/delivered_orders.html', {'orders': all_orders, 'category': category,
                                                     'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos, 'is_orderstatus': is_orderstatus,
                                                    'is_daily': is_daily})


@login_required
def undelivered_orders(request, category, id):
    all_orders = CustomerOrders.objects.all().filter(category_id=id, order_status__in=["Not Yet Specified", "UNDELIVERED", "OTHERS"]).order_by('date', 'time').exclude(state="lagos")
    if request.user.username == "evelynn" :
        all_orders = CustomerOrders.objects.all().filter(status="URGENT", category_id=id, order_status__in=["", "UNDELIVERED", "OTHERS"]).order_by('date', 'time').exclude(state="lagos")
    else:
        if 'start_date' in request.GET:
            s_date = request.GET['start_date']
            e_date = request.GET['end_date']
            all_un_orders = CustomerOrders.objects.all().filter(date__range=[s_date, e_date], category_id=id, order_status__in=["Not Yet Specified", "UNDELIVERED", "OTHERS"]).order_by('date', 'time').exclude(state="lagos")
        else:
            s_date = None
            e_date = None
            all_un_orders = CustomerOrders.objects.all().filter(category_id=id, order_status__in=["Not Yet Specified", "UNDELIVERED", "OTHERS"]).order_by('date', 'time').exclude(state="lagos")
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    categories = Category.objects.all()
    #paginator = Paginator(all_orders, 10)
    #page = request.GET.get('page')
    #try:
       # ordersss = paginator.page(page)
    #except PageNotAnInteger:
       # ordersss = paginator.page(1)
    #except EmptyPage:
        #ordersss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/undelivered_orders.html', {'orders': all_un_orders, 'category': category,
                                                     'categories': categories, 'is_entry': is_entry, 'is_lagos': is_lagos,'is_orderstatus': is_orderstatus,
                                                    'is_daily': is_daily})


@login_required
def new_stock(request):
    categories = Category.objects.all()
    my_form =StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            form = my_form
            messages.success(request, ' Stock Entry Created Successfully, You can Add Another Stock Entry')
            return render(request, 'inventory/new_stock.html', {'form': form, 'categories': categories})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Form')
    else:
        form = my_form
    return render(request, 'inventory/new_stock.html', {
        'form': form, 'categories': categories
    })


@login_required
def all_stocks(request):
    categories = Category.objects.all()
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    all_stocks = Stock.objects.all()
    paginator = Paginator(all_stocks, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/all_stocks.html', {
        'orders': all_stocks,
        'orderss': orderss,
        'is_entry': is_entry,
        'is_lagos': is_lagos,
        'is_daily': is_daily,
        'is_orderstatus': is_orderstatus,
        'categories': categories
    })



@login_required
def add_stock(request, state, id):
    categories = Category.objects.all()
    if 'add' in request.GET:
        if 'ginger_me' in request.GET:
                ginger_me_new = request.GET['ginger_me']
                Stock.objects.filter(pk__in=id).update(ginger_me=F('ginger_me')+ginger_me_new, ginger_me_value=ginger_me_new)
                StockValues.objects.all().create(ginger_me_value=ginger_me_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        elif 'cocoa_my_koko' in request.GET:
                cocoa_my_koko_new = request.GET['cocoa_my_koko']
                Stock.objects.filter(pk__in=id).update(cocoa_my_koko=F('cocoa_my_koko')+cocoa_my_koko_new)
                StockValues.objects.all().create(cocoa_my_koko_value=cocoa_my_koko_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        elif 'green_with_envy' in request.GET:
                green_with_envy_new = request.GET['green_with_envy']
                Stock.objects.filter(pk__in=id).update(green_with_envy=F('green_with_envy')+green_with_envy_new)
                StockValues.objects.all().create(green_with_envy_value=green_with_envy_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        elif 'inighe' in request.GET:
                inighe_new = request.GET['inighe']
                Stock.objects.filter(pk__in=id).update(inighe=F('inighe')+inighe_new)
                StockValues.objects.all().create(inighe_value=inighe_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        elif 'la_vida_loca' in request.GET:
                la_vida_loca_new = request.GET['la_vida_loca']
                Stock.objects.filter(pk__in=id).update(la_vida_loca=F('la_vida_loca')+la_vida_loca_new)
                StockValues.objects.all().create(la_vida_loca_value=la_vida_loca_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        elif 'nutty_by_nature' in request.GET:
                nutty_by_nature_new = request.GET['nutty_by_nature']
                Stock.objects.filter(pk__in=id).update(nutty_by_nature=F('nutty_by_nature')+nutty_by_nature_new)
                StockValues.objects.all().create(nutty_by_nature_value=nutty_by_nature_new, date_added=today, name=state, stock_added="yes", stock_removed="no")
        else:
            triple_threat_new = request.GET['triple_threat']
            Stock.objects.filter(pk__in=id).update(triple_threat=F('lotion') + triple_threat_new)
            StockValues.objects.all().create(triple_threat_value=triple_threat_new, date_added=today, name=state,
                                             stock_added="yes", stock_removed="no")

    elif 'remove' in request.GET:
        if 'ginger_me' in request.GET:
                ginger_me_new = request.GET['ginger_me']
                Stock.objects.filter(pk__in=id).update(ginger_me=F('ginger_me')-ginger_me_new)
                StockValues.objects.all().create(ginger_me_value=ginger_me_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        elif 'cocoa_my_koko' in request.GET:
                cocoa_my_koko_new = request.GET['cocoa_my_koko']
                Stock.objects.filter(pk__in=id).update(cocoa_my_koko=F('cocoa_my_koko')-cocoa_my_koko_new)
                StockValues.objects.all().create(cocoa_my_koko_value=cocoa_my_koko_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        elif 'green_with_envy' in request.GET:
                green_with_envy_new = request.GET['green_with_envy']
                Stock.objects.filter(pk__in=id).update(green_with_envy=F('green_with_envy')-green_with_envy_new)
                StockValues.objects.all().create(green_with_envy_value=green_with_envy_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        elif 'inighe' in request.GET:
                inighe_new = request.GET['inighe']
                Stock.objects.filter(pk__in=id).update(inighe=F('inighe')-inighe_new)
                StockValues.objects.all().create(inighe_value=inighe_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        elif 'la_vida_loca' in request.GET:
                la_vida_loca_new = request.GET['la_vida_loca']
                Stock.objects.filter(pk__in=id).update(la_vida_loca=F('la_vida_loca')-la_vida_loca_new)
                StockValues.objects.all().create(la_vida_loca_value=la_vida_loca_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        elif 'nutty_by_nature' in request.GET:
                nutty_by_nature_new = request.GET['nutty_by_nature']
                Stock.objects.filter(pk__in=id).update(nutty_by_nature=F('nutty_by_nature')-nutty_by_nature_new)
                StockValues.objects.all().create(nutty_by_nature_value=nutty_by_nature_new, date_added=today, name=state, stock_added="no", stock_removed="yes")
        else:
                triple_threat_new = request.GET['triple_threat']
                Stock.objects.filter(pk__in=id).update(triple_threat=F('triple_threat')-triple_threat_new)
                StockValues.objects.all().create(triple_threat_value=triple_threat_new, date_added=today, name=state, stock_added="no", stock_removed="yes")

    elif 'total' in request.GET:
        if 'totalamount' in request.GET:
            total_new = request.GET['totalamount']
            Stock.objects.filter(pk__in=id).update(total=total_new)
            StockValues.objects.all().create(total_value=total_new, date_added=today, name=state)

    else:
        remarks_new = request.GET['remarksname']
        Stock.objects.filter(pk__in=id).update(remarks=remarks_new)
        StockValues.objects.all().create(remarks_value=remarks_new, date_added=today, name=state)



    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_orderstatus = request.user.groups.filter(name='orderstatus').exists()
    all_stocks = Stock.objects.all()
    paginator = Paginator(all_stocks, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    messages.success(request, ' Stock Updated Successfully')
    return render(request, 'inventory/all_stocks.html', {'orders': all_stocks,'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos, 'is_orderstatus': is_orderstatus,
                                                    'is_daily': is_daily, 'categories': categories})


@login_required
def coms_exec_undelivered_orders(request, user):
    all_orders = CustomerOrders.objects.filter(coms_exec=user).order_by('-date', '-time').exclude(order_status="DELIVERED")
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    is_vieworders = request.user.groups.filter(name='vieworders').exists()
    categories = Category.objects.all()
    paginator = Paginator(all_orders, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/orders.html', {'orders': all_orders,
                                                     'categories': categories, 'orderss': orderss, 'is_entry': is_entry, 'is_lagos': is_lagos,
                                                    'is_daily': is_daily, 'is_vieworders': is_vieworders})


@login_required
def daily_by_state(request):
    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()

    product_value_total = CustomerOrders.objects.filter( date_added=today).aggregate(Sum('product_value'))

    t_orders_Jakande = CustomerOrders.objects.filter( state='Jakande', date_added=today).aggregate(Sum('product_value'))
    t_orders_Sangotedo = CustomerOrders.objects.filter( state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    t_orders_Eleko = CustomerOrders.objects.filter( state='Eleko', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ajah = CustomerOrders.objects.filter( state='Ajah', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ogba = CustomerOrders.objects.filter( state='Ogba', date_added=today).aggregate(Sum('product_value'))
    t_orders_Aguda = CustomerOrders.objects.filter( state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ketu = CustomerOrders.objects.filter( state='Ketu', date_added=today).aggregate(Sum('product_value'))
    t_orders_VI = CustomerOrders.objects.filter( state='VI', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikotun = CustomerOrders.objects.filter( state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    t_orders_Oshodi = CustomerOrders.objects.filter( state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikeja = CustomerOrders.objects.filter( state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    t_orders_Lekki = CustomerOrders.objects.filter( state='Lekki', date_added=today).aggregate(Sum('product_value'))
    t_orders_Apapa = CustomerOrders.objects.filter( state='Apapa', date_added=today).aggregate(Sum('product_value'))

    t_orders_abia = CustomerOrders.objects.filter( state='abia', date_added=today).aggregate(Sum('product_value'))
    t_orders_adamawa = CustomerOrders.objects.filter( state='adamawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_anambra = CustomerOrders.objects.filter( state='anambra', date_added=today).aggregate(Sum('product_value'))
    t_orders_akwa_ibom = CustomerOrders.objects.filter( state='akwa-ibom', date_added=today).aggregate(Sum('product_value'))
    t_orders_bauchi = CustomerOrders.objects.filter( state='bauchi', date_added=today).aggregate(Sum('product_value'))
    t_orders_bayelsa = CustomerOrders.objects.filter( state='bayelsa', date_added=today).aggregate(Sum('product_value'))
    t_orders_benue = CustomerOrders.objects.filter( state='benue', date_added=today).aggregate(Sum('product_value'))
    t_orders_borno = CustomerOrders.objects.filter( state='borno', date_added=today).aggregate(Sum('product_value'))
    t_orders_cross_river = CustomerOrders.objects.filter( state='cross-river', date_added=today).aggregate(Sum('product_value'))
    t_orders_delta = CustomerOrders.objects.filter( state='delta', date_added=today).aggregate(Sum('product_value'))
    t_orders_ebonyi = CustomerOrders.objects.filter( state='ebonyi', date_added=today).aggregate(Sum('product_value'))
    t_orders_enugu = CustomerOrders.objects.filter( state='enugu', date_added=today).aggregate(Sum('product_value'))
    t_orders_edo = CustomerOrders.objects.filter( state='edo', date_added=today).aggregate(Sum('product_value'))
    t_orders_ekiti = CustomerOrders.objects.filter( state='ekiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_gombe = CustomerOrders.objects.filter( state='gombe', date_added=today).aggregate(Sum('product_value'))
    t_orders_imo = CustomerOrders.objects.filter( state='imo', date_added=today).aggregate(Sum('product_value'))
    t_orders_jigawa = CustomerOrders.objects.filter( state='jigawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_kaduna = CustomerOrders.objects.filter( state='kaduna', date_added=today).aggregate(Sum('product_value'))
    t_orders_kano = CustomerOrders.objects.filter( state='kano', date_added=today).aggregate(Sum('product_value'))
    t_orders_katsina = CustomerOrders.objects.filter( state='katsina', date_added=today).aggregate(Sum('product_value'))
    t_orders_kebbi = CustomerOrders.objects.filter( state='kebbi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kogi = CustomerOrders.objects.filter( state='kogi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kwara = CustomerOrders.objects.filter( state='kwara', date_added=today).aggregate(Sum('product_value'))
    t_orders_lagos = CustomerOrders.objects.filter( state='lagos', date_added=today).aggregate(Sum('product_value'))
    t_orders_nasarawa = CustomerOrders.objects.filter( state='nasarawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter( state='niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_ogun = CustomerOrders.objects.filter( state='ogun', date_added=today).aggregate(Sum('product_value'))
    t_orders_ondo = CustomerOrders.objects.filter( state='ondo', date_added=today).aggregate(Sum('product_value'))
    t_orders_osun = CustomerOrders.objects.filter( state='osun', date_added=today).aggregate(Sum('product_value'))
    t_orders_oyo = CustomerOrders.objects.filter( state='oyo', date_added=today).aggregate(Sum('product_value'))
    t_orders_plateau = CustomerOrders.objects.filter( state='plateau', date_added=today).aggregate(Sum('product_value'))
    t_orders_rivers = CustomerOrders.objects.filter( state='rivers', date_added=today).aggregate(Sum('product_value'))
    t_orders_sokoto = CustomerOrders.objects.filter( state='sokoto', date_added=today).aggregate(Sum('product_value'))
    t_orders_taraba = CustomerOrders.objects.filter( state='taraba', date_added=today).aggregate(Sum('product_value'))
    t_orders_yobe = CustomerOrders.objects.filter( state='yobe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zamfara= CustomerOrders.objects.filter( state='zamfara', date_added=today).aggregate(Sum('product_value'))
    t_orders_abuja = CustomerOrders.objects.filter( state='abuja', date_added=today).aggregate(Sum('product_value'))
    t_orders_spain = CustomerOrders.objects.filter( state='spain', date_added=today).aggregate(Sum('product_value'))
    t_orders_usa = CustomerOrders.objects.filter( state='USA', date_added=today).aggregate(Sum('product_value'))
    t_orders_uk = CustomerOrders.objects.filter( state='UK', date_added=today).aggregate(Sum('product_value'))
    t_orders_ghana = CustomerOrders.objects.filter( state='Ghana', date_added=today).aggregate(Sum('product_value'))
    t_orders_canada = CustomerOrders.objects.filter( state='canada', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter( state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_saudi = CustomerOrders.objects.filter( state='Saudi Arabia', date_added=today).aggregate(Sum('product_value'))
    t_orders_south = CustomerOrders.objects.filter( state='South Africa', date_added=today).aggregate(Sum('product_value'))
    t_orders_switzerland = CustomerOrders.objects.filter( state='Switzerland', date_added=today).aggregate(Sum('product_value'))
    t_orders_turkey = CustomerOrders.objects.filter( state='Turkey', date_added=today).aggregate(Sum('product_value'))

    t_orders_zimbabwe = CustomerOrders.objects.filter( state='Zimbabwe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zambia = CustomerOrders.objects.filter( state='Zambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_yemen = CustomerOrders.objects.filter( state='Yemen', date_added=today).aggregate(Sum('product_value'))
    t_orders_venezuela = CustomerOrders.objects.filter( state='Venezuela', date_added=today).aggregate(Sum('product_value'))
    t_orders_uzbekistan = CustomerOrders.objects.filter( state='Uzbekistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_uruguay = CustomerOrders.objects.filter( state='Uruguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_uae = CustomerOrders.objects.filter( state='United Arab Emirates', date_added=today).aggregate(Sum('product_value'))
    t_orders_ukraine = CustomerOrders.objects.filter( state='Ukraine', date_added=today).aggregate(Sum('product_value'))
    t_orders_uganda = CustomerOrders.objects.filter( state='Uganda', date_added=today).aggregate(Sum('product_value'))
    t_orders_tunisia = CustomerOrders.objects.filter( state='Tunisia', date_added=today).aggregate(Sum('product_value'))
    t_orders_trinidad = CustomerOrders.objects.filter( state='Trinidad and Tobago', date_added=today).aggregate(Sum('product_value'))
    t_orders_togo = CustomerOrders.objects.filter( state='Togo', date_added=today).aggregate(Sum('product_value'))
    t_orders_thailand = CustomerOrders.objects.filter( state='Thailand', date_added=today).aggregate(Sum('product_value'))
    t_orders_tanzania = CustomerOrders.objects.filter( state='Tanzania', date_added=today).aggregate(Sum('product_value'))
    t_orders_taiwan = CustomerOrders.objects.filter( state='Taiwan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sweden = CustomerOrders.objects.filter( state='Sweden', date_added=today).aggregate(Sum('product_value'))
    t_orders_swaziland = CustomerOrders.objects.filter( state='Swaziland', date_added=today).aggregate(Sum('product_value'))
    t_orders_sudan = CustomerOrders.objects.filter( state='Sudan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sri = CustomerOrders.objects.filter( state='Sri Lanka', date_added=today).aggregate(Sum('product_value'))
    t_orders_somalia = CustomerOrders.objects.filter( state='Somalia', date_added=today).aggregate(Sum('product_value'))
    t_orders_solomon = CustomerOrders.objects.filter( state='Solomon Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovenia = CustomerOrders.objects.filter( state='Slovenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovakia = CustomerOrders.objects.filter( state='Slovakia', date_added=today).aggregate(Sum('product_value'))
    t_orders_singapore = CustomerOrders.objects.filter( state='Singapore', date_added=today).aggregate(Sum('product_value'))
    t_orders_sierra = CustomerOrders.objects.filter( state='Sierra Leone', date_added=today).aggregate(Sum('product_value'))
    t_orders_serbia = CustomerOrders.objects.filter( state='Serbia', date_added=today).aggregate(Sum('product_value'))
    t_orders_senegal = CustomerOrders.objects.filter( state='Senegal', date_added=today).aggregate(Sum('product_value'))
    t_orders_san = CustomerOrders.objects.filter( state='San Marino', date_added=today).aggregate(Sum('product_value'))
    t_orders_rwanda = CustomerOrders.objects.filter( state='Rwanda', date_added=today).aggregate(Sum('product_value'))
    t_orders_russia = CustomerOrders.objects.filter( state='Russian Federation', date_added=today).aggregate(Sum('product_value'))
    t_orders_romania = CustomerOrders.objects.filter( state='Romania', date_added=today).aggregate(Sum('product_value'))
    t_orders_qatar = CustomerOrders.objects.filter( state='Qatar', date_added=today).aggregate(Sum('product_value'))
    t_orders_portugal = CustomerOrders.objects.filter( state='Portugal', date_added=today).aggregate(Sum('product_value'))
    t_orders_poland = CustomerOrders.objects.filter( state='Poland', date_added=today).aggregate(Sum('product_value'))
    t_orders_philippines = CustomerOrders.objects.filter( state='Philippines', date_added=today).aggregate(Sum('product_value'))
    t_orders_peru = CustomerOrders.objects.filter( state='Peru', date_added=today).aggregate(Sum('product_value'))
    t_orders_paraguay = CustomerOrders.objects.filter( state='Paraguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_pakistan = CustomerOrders.objects.filter( state='Pakistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_oman = CustomerOrders.objects.filter( state='Oman', date_added=today).aggregate(Sum('product_value'))
    t_orders_norway = CustomerOrders.objects.filter( state='Norway', date_added=today).aggregate(Sum('product_value'))
    t_orders_niue = CustomerOrders.objects.filter( state='Niue', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter( state='Niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_nicaragua = CustomerOrders.objects.filter( state='Nicaragua', date_added=today).aggregate(Sum('product_value'))
    t_orders_newz = CustomerOrders.objects.filter( state='New Zealand', date_added=today).aggregate(Sum('product_value'))
    t_orders_netherlands = CustomerOrders.objects.filter( state='Netherlands', date_added=today).aggregate(Sum('product_value'))
    t_orders_nepal = CustomerOrders.objects.filter( state='Nepal', date_added=today).aggregate(Sum('product_value'))
    t_orders_namibia = CustomerOrders.objects.filter( state='Namibia', date_added=today).aggregate(Sum('product_value'))
    t_orders_mozambique = CustomerOrders.objects.filter( state='Mozambique', date_added=today).aggregate(Sum('product_value'))
    t_orders_morocco = CustomerOrders.objects.filter( state='Morocco', date_added=today).aggregate(Sum('product_value'))
    t_orders_montenegro = CustomerOrders.objects.filter( state='Montenegro', date_added=today).aggregate(Sum('product_value'))
    t_orders_mongolia = CustomerOrders.objects.filter( state='Mongolia', date_added=today).aggregate(Sum('product_value'))
    t_orders_moldova = CustomerOrders.objects.filter( state='Moldova', date_added=today).aggregate(Sum('product_value'))
    t_orders_mexico = CustomerOrders.objects.filter( state='Mexico', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritius = CustomerOrders.objects.filter( state='Mauritius', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritania = CustomerOrders.objects.filter( state='Mauritania', date_added=today).aggregate(Sum('product_value'))
    t_orders_malta = CustomerOrders.objects.filter( state='Malta', date_added=today).aggregate(Sum('product_value'))
    t_orders_mali = CustomerOrders.objects.filter( state='Mali', date_added=today).aggregate(Sum('product_value'))
    t_orders_malaysia = CustomerOrders.objects.filter( state='Malaysia', date_added=today).aggregate(Sum('product_value'))
    t_orders_malawi = CustomerOrders.objects.filter( state='Malawi', date_added=today).aggregate(Sum('product_value'))
    t_orders_madagascar = CustomerOrders.objects.filter( state='Madagascar', date_added=today).aggregate(Sum('product_value'))
    t_orders_luxembourg = CustomerOrders.objects.filter( state='Luxembourg', date_added=today).aggregate(Sum('product_value'))
    t_orders_lithuania = CustomerOrders.objects.filter( state='Lithuania', date_added=today).aggregate(Sum('product_value'))
    t_orders_liechtenstein = CustomerOrders.objects.filter( state='Liechtenstein', date_added=today).aggregate(Sum('product_value'))
    t_orders_libya = CustomerOrders.objects.filter( state='Libya', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_lesotho = CustomerOrders.objects.filter( state='Lesotho', date_added=today).aggregate(Sum('product_value'))
    t_orders_lebanon = CustomerOrders.objects.filter( state='Lebanon', date_added=today).aggregate(Sum('product_value'))
    t_orders_latvia = CustomerOrders.objects.filter( state='Latvia', date_added=today).aggregate(Sum('product_value'))
    t_orders_kuwait = CustomerOrders.objects.filter( state='Kuwait', date_added=today).aggregate(Sum('product_value'))
    t_orders_korea = CustomerOrders.objects.filter( state='Korea', date_added=today).aggregate(Sum('product_value'))
    t_orders_kenya = CustomerOrders.objects.filter( state='Kenya', date_added=today).aggregate(Sum('product_value'))
    t_orders_kazakhstan = CustomerOrders.objects.filter( state='Kazakhstan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jordan = CustomerOrders.objects.filter( state='Jordan', date_added=today).aggregate(Sum('product_value'))
    t_orders_japan = CustomerOrders.objects.filter( state='Japan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jamaica = CustomerOrders.objects.filter( state='Jamaica', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_israel = CustomerOrders.objects.filter( state='Israel', date_added=today).aggregate(Sum('product_value'))
    t_orders_ireland = CustomerOrders.objects.filter( state='Ireland', date_added=today).aggregate(Sum('product_value'))
    t_orders_iran = CustomerOrders.objects.filter( state='Iran', date_added=today).aggregate(Sum('product_value'))
    t_orders_iraq = CustomerOrders.objects.filter( state='Iraq', date_added=today).aggregate(Sum('product_value'))
    t_orders_indonesia = CustomerOrders.objects.filter( state='Indonesia', date_added=today).aggregate(Sum('product_value'))
    t_orders_india = CustomerOrders.objects.filter( state='India', date_added=today).aggregate(Sum('product_value'))
    t_orders_iceland = CustomerOrders.objects.filter( state='Iceland', date_added=today).aggregate(Sum('product_value'))
    t_orders_hungary = CustomerOrders.objects.filter( state='Hungary', date_added=today).aggregate(Sum('product_value'))
    t_orders_hong = CustomerOrders.objects.filter( state='Hong Kong', date_added=today).aggregate(Sum('product_value'))
    t_orders_honduras = CustomerOrders.objects.filter( state='Honduras', date_added=today).aggregate(Sum('product_value'))
    t_orders_haiti = CustomerOrders.objects.filter( state='Haiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_guineab = CustomerOrders.objects.filter( state='Guinea-Bissau', date_added=today).aggregate(Sum('product_value'))
    t_orders_guinea = CustomerOrders.objects.filter( state='Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_guatemala = CustomerOrders.objects.filter( state='Guatemala', date_added=today).aggregate(Sum('product_value'))
    t_orders_greenland = CustomerOrders.objects.filter( state='Greenland', date_added=today).aggregate(Sum('product_value'))
    t_orders_greece = CustomerOrders.objects.filter( state='Greece', date_added=today).aggregate(Sum('product_value'))
    t_orders_gibraltar = CustomerOrders.objects.filter( state='Gibraltar', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_georgia = CustomerOrders.objects.filter( state='Georgia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gambia = CustomerOrders.objects.filter( state='Gambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gabon = CustomerOrders.objects.filter( state='Gabon', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter( state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_finland = CustomerOrders.objects.filter( state='Finland', date_added=today).aggregate(Sum('product_value'))
    t_orders_faroe = CustomerOrders.objects.filter( state='Faroe Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_ethiopia = CustomerOrders.objects.filter( state='Ethiopia', date_added=today).aggregate(Sum('product_value'))
    t_orders_estonia = CustomerOrders.objects.filter( state='Estonia', date_added=today).aggregate(Sum('product_value'))
    t_orders_eritrea = CustomerOrders.objects.filter( state='Eritrea', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_els = CustomerOrders.objects.filter( state='El Salvador', date_added=today).aggregate(Sum('product_value'))
    t_orders_egypt = CustomerOrders.objects.filter( state='Egypt', date_added=today).aggregate(Sum('product_value'))
    t_orders_ecuador = CustomerOrders.objects.filter( state='Ecuador', date_added=today).aggregate(Sum('product_value'))
    t_orders_denmark = CustomerOrders.objects.filter( state='Denmark', date_added=today).aggregate(Sum('product_value'))
    t_orders_czech = CustomerOrders.objects.filter( state='Czech Republic', date_added=today).aggregate(Sum('product_value'))
    t_orders_cyprus = CustomerOrders.objects.filter( state='Cyprus', date_added=today).aggregate(Sum('product_value'))
    t_orders_cuba = CustomerOrders.objects.filter( state='Cuba', date_added=today).aggregate(Sum('product_value'))
    t_orders_croatia = CustomerOrders.objects.filter( state='Croatia', date_added=today).aggregate(Sum('product_value'))
    t_orders_ivory = CustomerOrders.objects.filter( state='Ivory Coast', date_added=today).aggregate(Sum('product_value'))
    t_orders_costa = CustomerOrders.objects.filter( state='Costa Rica', date_added=today).aggregate(Sum('product_value'))
    t_orders_congo = CustomerOrders.objects.filter( state='Congo', date_added=today).aggregate(Sum('product_value'))
    t_orders_colombia = CustomerOrders.objects.filter( state='Colombia', date_added=today).aggregate(Sum('product_value'))
    t_orders_christmas = CustomerOrders.objects.filter( state='Christmas Island', date_added=today).aggregate(Sum('product_value'))
    t_orders_china = CustomerOrders.objects.filter( state='China', date_added=today).aggregate(Sum('product_value'))
    t_orders_chile = CustomerOrders.objects.filter( state='Chile', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_chad = CustomerOrders.objects.filter( state='Chad', date_added=today).aggregate(Sum('product_value'))
    t_orders_central = CustomerOrders.objects.filter( state='Central African Republi', date_added=today).aggregate(Sum('product_value'))
    t_orders_cape = CustomerOrders.objects.filter( state='Cape Verde', date_added=today).aggregate(Sum('product_value'))
    t_orders_cameroo = CustomerOrders.objects.filter( state='Cameroo', date_added=today).aggregate(Sum('product_value'))
    t_orders_burundi = CustomerOrders.objects.filter( state='Burundi', date_added=today).aggregate(Sum('product_value'))
    t_orders_burkina = CustomerOrders.objects.filter( state='Burkina Faso', date_added=today).aggregate(Sum('product_value'))
    t_orders_bulgaria = CustomerOrders.objects.filter( state='Bulgaria', date_added=today).aggregate(Sum('product_value'))
    t_orders_brazil = CustomerOrders.objects.filter( state='Brazil', date_added=today).aggregate(Sum('product_value'))
    t_orders_botswana = CustomerOrders.objects.filter( state='Botswana', date_added=today).aggregate(Sum('product_value'))
    t_orders_bosnia = CustomerOrders.objects.filter( state='Bosnia and Herzegovina', date_added=today).aggregate(Sum('product_value'))
    t_orders_bolivia = CustomerOrders.objects.filter( state='Bolivia', date_added=today).aggregate(Sum('product_value'))
    t_orders_benin = CustomerOrders.objects.filter( state='Benin', date_added=today).aggregate(Sum('product_value'))
    t_orders_belgium = CustomerOrders.objects.filter( state='Belgium', date_added=today).aggregate(Sum('product_value'))
    t_orders_belarus = CustomerOrders.objects.filter( state='Belarus', date_added=today).aggregate(Sum('product_value'))
    t_orders_barbados = CustomerOrders.objects.filter( state='Barbados', date_added=today).aggregate(Sum('product_value'))
    t_orders_bangladesh = CustomerOrders.objects.filter( state='Bangladesh', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahrain = CustomerOrders.objects.filter( state='Bahrain', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahamas = CustomerOrders.objects.filter( state='Bahamas', date_added=today).aggregate(Sum('product_value'))
    t_orders_azerbaija = CustomerOrders.objects.filter( state='Azerbaija', date_added=today).aggregate(Sum('product_value'))
    t_orders_austria = CustomerOrders.objects.filter( state='Austria', date_added=today).aggregate(Sum('product_value'))
    t_orders_australi = CustomerOrders.objects.filter( state='Australi', date_added=today).aggregate(Sum('product_value'))
    t_orders_armenia = CustomerOrders.objects.filter( state='Armenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_argentina = CustomerOrders.objects.filter( state='Argentina', date_added=today).aggregate(Sum('product_value'))
    t_orders_angola = CustomerOrders.objects.filter( state='Angola', date_added=today).aggregate(Sum('product_value'))
    t_orders_algeria = CustomerOrders.objects.filter( state='Algeria', date_added=today).aggregate(Sum('product_value'))
    t_orders_albania = CustomerOrders.objects.filter( state='Albania', date_added=today).aggregate(Sum('product_value'))
    t_orders_afghanistan = CustomerOrders.objects.filter( state='Afghanistan', date_added=today).aggregate(Sum('product_value'))


    product_value_total_y = CustomerOrders.objects.filter( date_added=yesterday).aggregate(Sum('product_value'))

    y_orders_Jakande = CustomerOrders.objects.filter( state='Jakande', date_added=today).aggregate(Sum('product_value'))
    y_orders_Sangotedo = CustomerOrders.objects.filter( state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    y_orders_Eleko = CustomerOrders.objects.filter( state='Eleko', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ajah = CustomerOrders.objects.filter( state='Ajah', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ogba = CustomerOrders.objects.filter( state='Ogba', date_added=today).aggregate(Sum('product_value'))
    y_orders_Aguda = CustomerOrders.objects.filter( state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ketu = CustomerOrders.objects.filter( state='Ketu', date_added=today).aggregate(Sum('product_value'))
    y_orders_VI = CustomerOrders.objects.filter( state='VI', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikotun = CustomerOrders.objects.filter( state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    y_orders_Oshodi = CustomerOrders.objects.filter( state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikeja = CustomerOrders.objects.filter( state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    y_orders_Lekki = CustomerOrders.objects.filter( state='Lekki', date_added=today).aggregate(Sum('product_value'))
    y_orders_Apapa = CustomerOrders.objects.filter( state='Apapa', date_added=today).aggregate(Sum('product_value'))

    y_orders_abia = CustomerOrders.objects.filter( state='abia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_adamawa = CustomerOrders.objects.filter( state='adamawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_anambra = CustomerOrders.objects.filter( state='anambra', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_akwa_ibom = CustomerOrders.objects.filter( state='akwa-ibom', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bauchi = CustomerOrders.objects.filter( state='bauchi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bayelsa = CustomerOrders.objects.filter( state='bayelsa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benue = CustomerOrders.objects.filter( state='benue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_borno = CustomerOrders.objects.filter( state='borno', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cross_river = CustomerOrders.objects.filter( state='cross-river', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_delta = CustomerOrders.objects.filter( state='delta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ebonyi = CustomerOrders.objects.filter( state='ebonyi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_enugu = CustomerOrders.objects.filter( state='enugu', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_edo = CustomerOrders.objects.filter( state='edo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ekiti = CustomerOrders.objects.filter( state='ekiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gombe = CustomerOrders.objects.filter( state='gombe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_imo = CustomerOrders.objects.filter( state='imo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jigawa = CustomerOrders.objects.filter( state='jigawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kaduna = CustomerOrders.objects.filter( state='kaduna', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kano = CustomerOrders.objects.filter( state='kano', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_katsina = CustomerOrders.objects.filter( state='katsina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kebbi = CustomerOrders.objects.filter( state='kebbi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kogi = CustomerOrders.objects.filter( state='kogi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kwara = CustomerOrders.objects.filter( state='kwara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lagos = CustomerOrders.objects.filter( state='lagos', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nasarawa = CustomerOrders.objects.filter( state='nasarawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter( state='niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ogun = CustomerOrders.objects.filter( state='ogun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ondo = CustomerOrders.objects.filter( state='ondo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_osun = CustomerOrders.objects.filter( state='osun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oyo = CustomerOrders.objects.filter( state='oyo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_plateau = CustomerOrders.objects.filter( state='plateau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rivers = CustomerOrders.objects.filter( state='rivers', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sokoto = CustomerOrders.objects.filter( state='sokoto', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taraba = CustomerOrders.objects.filter( state='taraba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yobe = CustomerOrders.objects.filter( state='yobe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zamfara= CustomerOrders.objects.filter( state='zamfara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_abuja = CustomerOrders.objects.filter( state='abuja', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_spain = CustomerOrders.objects.filter( state='spain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_usa = CustomerOrders.objects.filter( state='USA', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uk = CustomerOrders.objects.filter( state='UK', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ghana = CustomerOrders.objects.filter( state='Ghana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_canada = CustomerOrders.objects.filter( state='canada', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter( state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_saudi = CustomerOrders.objects.filter( state='Saudi Arabia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_south = CustomerOrders.objects.filter( state='South Africa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_switzerland = CustomerOrders.objects.filter( state='Switzerland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_turkey = CustomerOrders.objects.filter( state='Turkey', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zimbabwe = CustomerOrders.objects.filter( state='Zimbabwe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zambia = CustomerOrders.objects.filter( state='Zambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yemen = CustomerOrders.objects.filter( state='Yemen', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_venezuela = CustomerOrders.objects.filter( state='Venezuela', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uzbekistan = CustomerOrders.objects.filter( state='Uzbekistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uruguay = CustomerOrders.objects.filter( state='Uruguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uae = CustomerOrders.objects.filter( state='United Arab Emirates', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ukraine = CustomerOrders.objects.filter( state='Ukraine', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uganda = CustomerOrders.objects.filter( state='Uganda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tunisia = CustomerOrders.objects.filter( state='Tunisia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_trinidad = CustomerOrders.objects.filter( state='Trinidad and Tobago', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_togo = CustomerOrders.objects.filter( state='Togo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_thailand = CustomerOrders.objects.filter( state='Thailand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tanzania = CustomerOrders.objects.filter( state='Tanzania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taiwan = CustomerOrders.objects.filter( state='Taiwan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sweden = CustomerOrders.objects.filter( state='Sweden', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_swaziland = CustomerOrders.objects.filter( state='Swaziland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sudan = CustomerOrders.objects.filter( state='Sudan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sri = CustomerOrders.objects.filter( state='Sri Lanka', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_somalia = CustomerOrders.objects.filter( state='Somalia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_solomon = CustomerOrders.objects.filter( state='Solomon Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovenia = CustomerOrders.objects.filter( state='Slovenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovakia = CustomerOrders.objects.filter( state='Slovakia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_singapore = CustomerOrders.objects.filter( state='Singapore', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sierra = CustomerOrders.objects.filter( state='Sierra Leone', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_serbia = CustomerOrders.objects.filter( state='Serbia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_senegal = CustomerOrders.objects.filter( state='Senegal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_san = CustomerOrders.objects.filter( state='San Marino', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rwanda = CustomerOrders.objects.filter( state='Rwanda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_russia = CustomerOrders.objects.filter( state='Russian Federation', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_romania = CustomerOrders.objects.filter( state='Romania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_qatar = CustomerOrders.objects.filter( state='Qatar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_portugal = CustomerOrders.objects.filter( state='Portugal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_poland = CustomerOrders.objects.filter( state='Poland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_philippines = CustomerOrders.objects.filter( state='Philippines', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_peru = CustomerOrders.objects.filter( state='Peru', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_paraguay = CustomerOrders.objects.filter( state='Paraguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_pakistan = CustomerOrders.objects.filter( state='Pakistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oman = CustomerOrders.objects.filter( state='Oman', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_norway = CustomerOrders.objects.filter( state='Norway', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niue = CustomerOrders.objects.filter( state='Niue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter( state='Niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nicaragua = CustomerOrders.objects.filter( state='Nicaragua', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_newz = CustomerOrders.objects.filter( state='New Zealand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_netherlands = CustomerOrders.objects.filter( state='Netherlands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nepal = CustomerOrders.objects.filter( state='Nepal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_namibia = CustomerOrders.objects.filter( state='Namibia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mozambique = CustomerOrders.objects.filter( state='Mozambique', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_morocco = CustomerOrders.objects.filter( state='Morocco', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_montenegro = CustomerOrders.objects.filter( state='Montenegro', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mongolia = CustomerOrders.objects.filter( state='Mongolia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_moldova = CustomerOrders.objects.filter( state='Moldova', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mexico = CustomerOrders.objects.filter( state='Mexico', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritius = CustomerOrders.objects.filter( state='Mauritius', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritania = CustomerOrders.objects.filter( state='Mauritania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malta = CustomerOrders.objects.filter( state='Malta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mali = CustomerOrders.objects.filter( state='Mali', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malaysia = CustomerOrders.objects.filter( state='Malaysia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malawi = CustomerOrders.objects.filter( state='Malawi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_madagascar = CustomerOrders.objects.filter( state='Madagascar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_luxembourg = CustomerOrders.objects.filter( state='Luxembourg', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lithuania = CustomerOrders.objects.filter( state='Lithuania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liechtenstein = CustomerOrders.objects.filter( state='Liechtenstein', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_libya = CustomerOrders.objects.filter( state='Libya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lesotho = CustomerOrders.objects.filter( state='Lesotho', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lebanon = CustomerOrders.objects.filter( state='Lebanon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_latvia = CustomerOrders.objects.filter( state='Latvia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kuwait = CustomerOrders.objects.filter( state='Kuwait', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_korea = CustomerOrders.objects.filter( state='Korea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kenya = CustomerOrders.objects.filter( state='Kenya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kazakhstan = CustomerOrders.objects.filter( state='Kazakhstan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jordan = CustomerOrders.objects.filter( state='Jordan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_japan = CustomerOrders.objects.filter( state='Japan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jamaica = CustomerOrders.objects.filter( state='Jamaica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_israel = CustomerOrders.objects.filter( state='Israel', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ireland = CustomerOrders.objects.filter( state='Ireland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iran = CustomerOrders.objects.filter( state='Iran', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iraq = CustomerOrders.objects.filter( state='Iraq', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_indonesia = CustomerOrders.objects.filter( state='Indonesia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_india = CustomerOrders.objects.filter( state='India', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iceland = CustomerOrders.objects.filter( state='Iceland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hungary = CustomerOrders.objects.filter( state='Hungary', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hong = CustomerOrders.objects.filter( state='Hong Kong', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_honduras = CustomerOrders.objects.filter( state='Honduras', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_haiti = CustomerOrders.objects.filter( state='Haiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guineab = CustomerOrders.objects.filter( state='Guinea-Bissau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guinea = CustomerOrders.objects.filter( state='Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guatemala = CustomerOrders.objects.filter( state='Guatemala', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greenland = CustomerOrders.objects.filter( state='Greenland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greece = CustomerOrders.objects.filter( state='Greece', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gibraltar = CustomerOrders.objects.filter( state='Gibraltar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_georgia = CustomerOrders.objects.filter( state='Georgia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gambia = CustomerOrders.objects.filter( state='Gambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gabon = CustomerOrders.objects.filter( state='Gabon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter( state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_finland = CustomerOrders.objects.filter( state='Finland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_faroe = CustomerOrders.objects.filter( state='Faroe Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ethiopia = CustomerOrders.objects.filter( state='Ethiopia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_estonia = CustomerOrders.objects.filter( state='Estonia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_eritrea = CustomerOrders.objects.filter( state='Eritrea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_els = CustomerOrders.objects.filter( state='El Salvador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_egypt = CustomerOrders.objects.filter( state='Egypt', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ecuador = CustomerOrders.objects.filter( state='Ecuador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_denmark = CustomerOrders.objects.filter( state='Denmark', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_czech = CustomerOrders.objects.filter( state='Czech Republic', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cyprus = CustomerOrders.objects.filter( state='Cyprus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cuba = CustomerOrders.objects.filter( state='Cuba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_croatia = CustomerOrders.objects.filter( state='Croatia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ivory = CustomerOrders.objects.filter( state='Ivory Coast', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_costa = CustomerOrders.objects.filter( state='Costa Rica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_congo = CustomerOrders.objects.filter( state='Congo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_colombia = CustomerOrders.objects.filter( state='Colombia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_christmas = CustomerOrders.objects.filter( state='Christmas Island', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_china = CustomerOrders.objects.filter( state='China', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chile = CustomerOrders.objects.filter( state='Chile', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chad = CustomerOrders.objects.filter( state='Chad', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_central = CustomerOrders.objects.filter( state='Central African Republi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cape = CustomerOrders.objects.filter( state='Cape Verde', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cameroo = CustomerOrders.objects.filter( state='Cameroo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burundi = CustomerOrders.objects.filter( state='Burundi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burkina = CustomerOrders.objects.filter( state='Burkina Faso', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bulgaria = CustomerOrders.objects.filter( state='Bulgaria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_brazil = CustomerOrders.objects.filter( state='Brazil', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_botswana = CustomerOrders.objects.filter( state='Botswana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bosnia = CustomerOrders.objects.filter( state='Bosnia and Herzegovina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bolivia = CustomerOrders.objects.filter( state='Bolivia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benin = CustomerOrders.objects.filter( state='Benin', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belgium = CustomerOrders.objects.filter( state='Belgium', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belarus = CustomerOrders.objects.filter( state='Belarus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_barbados = CustomerOrders.objects.filter( state='Barbados', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bangladesh = CustomerOrders.objects.filter( state='Bangladesh', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahrain = CustomerOrders.objects.filter( state='Bahrain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahamas = CustomerOrders.objects.filter( state='Bahamas', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_azerbaija = CustomerOrders.objects.filter( state='Azerbaija', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_austria = CustomerOrders.objects.filter( state='Austria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_australi = CustomerOrders.objects.filter( state='Australi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_armenia = CustomerOrders.objects.filter( state='Armenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_argentina = CustomerOrders.objects.filter( state='Argentina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_angola = CustomerOrders.objects.filter( state='Angola', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_algeria = CustomerOrders.objects.filter( state='Algeria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_albania = CustomerOrders.objects.filter( state='Albania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_afghanistan = CustomerOrders.objects.filter( state='Afghanistan', date_added=yesterday).aggregate(Sum('product_value'))


    return render(request, 'inventory/daily_orders_state.html', {'categories': categories,

                                                            't_orders_Jakande' :  t_orders_Jakande,
                                                            't_orders_Sangotedo': t_orders_Sangotedo,
                                                            't_orders_Eleko': t_orders_Eleko,
                                                            't_orders_Ajah': t_orders_Ajah,
                                                            't_orders_Ogba': t_orders_Ogba,
                                                            't_orders_Aguda': t_orders_Aguda,
                                                            't_orders_Ketu': t_orders_Ketu,
                                                            't_orders_VI': t_orders_VI,
                                                            't_orders_Ikotun': t_orders_Ikotun,
                                                            't_orders_Oshodi': t_orders_Oshodi,
                                                            't_orders_Ikeja': t_orders_Ikeja,
                                                            't_orders_Lekki': t_orders_Lekki ,
                                                            't_orders_Apapa': t_orders_Apapa,


                                                            't_orders_abia': t_orders_abia,
                                                            't_orders_adamawa': t_orders_adamawa,
                                                            't_orders_anambra': t_orders_anambra,
                                                            't_orders_akwa_ibom': t_orders_akwa_ibom,
                                                            't_orders_bauchi': t_orders_bauchi,
                                                            't_orders_bayelsa': t_orders_bayelsa,
                                                            't_orders_benue': t_orders_benue,
                                                            't_orders_borno': t_orders_borno,
                                                            't_orders_cross_river': t_orders_cross_river,
                                                            't_orders_delta': t_orders_delta,
                                                            't_orders_ebonyi': t_orders_ebonyi,
                                                            't_orders_enugu': t_orders_enugu,
                                                            't_orders_edo': t_orders_edo,
                                                            't_orders_ekiti': t_orders_ekiti,
                                                            't_orders_gombe': t_orders_gombe,
                                                            't_orders_imo': t_orders_imo,
                                                            't_orders_jigawa': t_orders_jigawa,
                                                            't_orders_kaduna': t_orders_kaduna,
                                                            't_orders_kano': t_orders_kano,
                                                            't_orders_katsina': t_orders_katsina,
                                                            't_orders_kebbi': t_orders_kebbi,
                                                            't_orders_kogi': t_orders_kogi,
                                                            't_orders_kwara': t_orders_kwara,
                                                            't_orders_lagos': t_orders_lagos,
                                                            't_orders_nasarawa': t_orders_nasarawa,
                                                            't_orders_niger': t_orders_niger,
                                                            't_orders_ogun': t_orders_ogun,
                                                            't_orders_ondo': t_orders_ondo,
                                                            't_orders_osun': t_orders_osun,
                                                            't_orders_oyo': t_orders_oyo,
                                                            't_orders_plateau': t_orders_plateau,
                                                            't_orders_rivers': t_orders_rivers,
                                                            't_orders_sokoto': t_orders_sokoto,
                                                            't_orders_taraba': t_orders_taraba,
                                                            't_orders_yobe': t_orders_yobe,
                                                            't_orders_zamfara': t_orders_zamfara,
                                                            't_orders_abuja': t_orders_abuja,
                                                            't_orders_spain': t_orders_spain,
                                                            't_orders_usa': t_orders_usa,
                                                            't_orders_uk': t_orders_uk,
                                                            't_orders_ghana': t_orders_ghana,
                                                            't_orders_canada': t_orders_canada,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_saudi': t_orders_saudi,
                                                            't_orders_south': t_orders_south,
                                                            't_orders_switzerland': t_orders_switzerland,
                                                            't_orders_turkey': t_orders_turkey,

                                                            't_orders_zimbabwe' : t_orders_zimbabwe,
                                                            't_orders_zambia':  t_orders_zambia,
                                                            't_orders_yemen': t_orders_yemen,
                                                            't_orders_venezuela': t_orders_venezuela,
                                                            't_orders_uzbekistan': t_orders_uzbekistan,
                                                            't_orders_uruguay': t_orders_uruguay,
                                                            't_orders_uae': t_orders_uae,
                                                            't_orders_ukraine': t_orders_ukraine,
                                                            't_orders_uganda': t_orders_uganda,
                                                            't_orders_tunisia': t_orders_tunisia,
                                                            't_orders_trinidad': t_orders_trinidad,
                                                            't_orders_togo': t_orders_togo,
                                                            't_orders_thailand': t_orders_thailand,
                                                            't_orders_tanzania': t_orders_tanzania,
                                                            't_orders_taiwan': t_orders_taiwan,
                                                            't_orders_sweden': t_orders_sweden,
                                                            't_orders_swaziland': t_orders_swaziland,
                                                            't_orders_sudan': t_orders_sudan,
                                                            't_orders_sri': t_orders_sri,
                                                            't_orders_somalia': t_orders_somalia,
                                                            't_orders_solomon': t_orders_solomon,
                                                            't_orders_slovenia': t_orders_slovenia,
                                                            't_orders_slovakia': t_orders_slovakia,
                                                            't_orders_singapore': t_orders_singapore,
                                                            't_orders_sierra': t_orders_sierra,
                                                            't_orders_serbia': t_orders_serbia,
                                                            't_orders_senegal': t_orders_senegal,
                                                            't_orders_san': t_orders_san,
                                                            't_orders_rwanda': t_orders_rwanda,
                                                            't_orders_russia': t_orders_russia,
                                                            't_orders_romania': t_orders_romania,
                                                            't_orders_qatar': t_orders_qatar,
                                                            't_orders_portugal': t_orders_portugal,
                                                            't_orders_poland': t_orders_poland,
                                                            't_orders_philippines': t_orders_philippines,
                                                            't_orders_peru': t_orders_peru,
                                                            't_orders_paraguay': t_orders_paraguay,
                                                            't_orders_pakistan': t_orders_pakistan,
                                                            't_orders_oman': t_orders_oman,
                                                            't_orders_norway': t_orders_norway,
                                                            't_orders_niue': t_orders_niue,
                                                            't_orders_niger':  t_orders_niger,
                                                            't_orders_nicaragua': t_orders_nicaragua,
                                                            't_orders_newz': t_orders_newz,
                                                            't_orders_netherlands': t_orders_netherlands,
                                                            't_orders_nepal': t_orders_nepal,
                                                            't_orders_namibia': t_orders_namibia,
                                                            't_orders_mozambique': t_orders_mozambique,
                                                            't_orders_morocco': t_orders_morocco,
                                                            't_orders_montenegro': t_orders_montenegro,
                                                            't_orders_mongolia': t_orders_mongolia,
                                                            't_orders_moldova': t_orders_moldova,
                                                            't_orders_mexico': t_orders_mexico,
                                                            't_orders_mauritius': t_orders_mauritius,
                                                            't_orders_mauritania': t_orders_mauritania,
                                                            't_orders_malta': t_orders_malta,
                                                            't_orders_mali': t_orders_mali,
                                                            't_orders_malaysia': t_orders_malaysia,
                                                            't_orders_malawi': t_orders_malawi,
                                                            't_orders_madagascar': t_orders_madagascar,
                                                            't_orders_luxembourg': t_orders_luxembourg,
                                                            't_orders_lithuania': t_orders_lithuania,
                                                            't_orders_liechtenstein': t_orders_liechtenstein,
                                                            't_orders_libya': t_orders_libya,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_lesotho': t_orders_lesotho,
                                                            't_orders_lebanon': t_orders_lebanon,
                                                            't_orders_latvia': t_orders_latvia,
                                                            't_orders_kuwait': t_orders_kuwait,
                                                            't_orders_korea': t_orders_korea,
                                                            't_orders_kenya': t_orders_kenya,
                                                            't_orders_kazakhstan': t_orders_kazakhstan,
                                                            't_orders_jordan': t_orders_jordan,
                                                            't_orders_japan': t_orders_japan,
                                                            't_orders_jamaica': t_orders_jamaica,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_israel': t_orders_israel,
                                                            't_orders_ireland': t_orders_ireland,
                                                            't_orders_iran': t_orders_iran,
                                                            't_orders_iraq': t_orders_iraq,
                                                            't_orders_indonesia': t_orders_indonesia,
                                                            't_orders_india': t_orders_india,
                                                            't_orders_iceland': t_orders_iceland,
                                                            't_orders_hungary': t_orders_hungary,
                                                            't_orders_hong': t_orders_hong,
                                                            't_orders_honduras': t_orders_honduras,
                                                            't_orders_haiti': t_orders_haiti,
                                                            't_orders_guineab': t_orders_guineab,
                                                            't_orders_guinea': t_orders_guinea,
                                                            't_orders_guatemala': t_orders_guatemala,
                                                            't_orders_greenland': t_orders_greenland,
                                                            't_orders_greece': t_orders_greece,
                                                            't_orders_gibraltar': t_orders_gibraltar,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_georgia': t_orders_georgia,
                                                            't_orders_gambia': t_orders_gambia,
                                                            't_orders_gabon': t_orders_gabon,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_finland': t_orders_finland,
                                                            't_orders_faroe': t_orders_faroe,
                                                            't_orders_ethiopia': t_orders_ethiopia,
                                                            't_orders_estonia': t_orders_estonia,
                                                            't_orders_eritrea': t_orders_eritrea,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_els': t_orders_els,
                                                            't_orders_egypt': t_orders_egypt,
                                                            't_orders_ecuador': t_orders_ecuador,
                                                            't_orders_denmark': t_orders_denmark,
                                                            't_orders_czech': t_orders_czech,
                                                            't_orders_cyprus': t_orders_cyprus,
                                                            't_orders_cuba': t_orders_cuba,
                                                            't_orders_croatia': t_orders_croatia,
                                                            't_orders_ivory': t_orders_ivory,
                                                            't_orders_costa': t_orders_costa,
                                                            't_orders_congo': t_orders_congo,
                                                            't_orders_colombia': t_orders_colombia,
                                                            't_orders_christmas': t_orders_christmas,
                                                            't_orders_china': t_orders_china,
                                                            't_orders_chile': t_orders_chile,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_chad': t_orders_chad,
                                                            't_orders_central': t_orders_central,
                                                            't_orders_cape': t_orders_cape,
                                                            't_orders_cameroo': t_orders_cameroo,
                                                            't_orders_burundi': t_orders_burundi,
                                                            't_orders_burkina': t_orders_burkina,
                                                            't_orders_bulgaria': t_orders_bulgaria,
                                                            't_orders_brazil': t_orders_brazil,
                                                            't_orders_botswana': t_orders_botswana,
                                                            't_orders_bosnia': t_orders_bosnia,
                                                            't_orders_bolivia': t_orders_bolivia,
                                                            't_orders_benin': t_orders_benin,
                                                            't_orders_belgium': t_orders_belgium,
                                                            't_orders_belarus': t_orders_belarus,
                                                            't_orders_barbados': t_orders_barbados,
                                                            't_orders_bangladesh': t_orders_bangladesh,
                                                            't_orders_bahrain': t_orders_bahrain,
                                                            't_orders_bahamas': t_orders_bahamas,
                                                            't_orders_azerbaija': t_orders_azerbaija,
                                                            't_orders_austria': t_orders_austria,
                                                            't_orders_australi': t_orders_australi,
                                                            't_orders_armenia': t_orders_armenia,
                                                            't_orders_argentina': t_orders_argentina,
                                                            't_orders_angola': t_orders_angola,
                                                            't_orders_algeria': t_orders_algeria,
                                                            't_orders_albania': t_orders_albania,
                                                            't_orders_afghanistan': t_orders_afghanistan,

                                                            'y_orders_Jakande' :  y_orders_Jakande,
                                                            'y_orders_Sangotedo': y_orders_Sangotedo,
                                                            'y_orders_Eleko': y_orders_Eleko,
                                                            'y_orders_Ajah': y_orders_Ajah,
                                                            'y_orders_Ogba': y_orders_Ogba,
                                                            'y_orders_Aguda': y_orders_Aguda,
                                                            'y_orders_Ketu': y_orders_Ketu,
                                                            'y_orders_VI': y_orders_VI,
                                                            'y_orders_Ikotun': y_orders_Ikotun,
                                                            'y_orders_Oshodi': y_orders_Oshodi,
                                                            'y_orders_Ikeja': y_orders_Ikeja,
                                                            'y_orders_Lekki': y_orders_Lekki ,
                                                            'y_orders_Apapa': y_orders_Apapa,

                                                            'y_orders_zimbabwe' : y_orders_zimbabwe,
                                                            'y_orders_zambia':  y_orders_zambia,
                                                            'y_orders_yemen': y_orders_yemen,
                                                            'y_orders_venezuela': y_orders_venezuela,
                                                            'y_orders_uzbekistan': y_orders_uzbekistan,
                                                            'y_orders_uruguay': y_orders_uruguay,
                                                            'y_orders_uae': y_orders_uae,
                                                            'y_orders_ukraine': y_orders_ukraine,
                                                            'y_orders_uganda': y_orders_uganda,
                                                            'y_orders_tunisia': y_orders_tunisia,
                                                            'y_orders_trinidad': y_orders_trinidad,
                                                            'y_orders_togo': y_orders_togo,
                                                            'y_orders_thailand': y_orders_thailand,
                                                            'y_orders_tanzania': y_orders_tanzania,
                                                            'y_orders_taiwan': y_orders_taiwan,
                                                            'y_orders_sweden': y_orders_sweden,
                                                            'y_orders_swaziland': y_orders_swaziland,
                                                            'y_orders_sudan': y_orders_sudan,
                                                            'y_orders_sri': y_orders_sri,
                                                            'y_orders_somalia': y_orders_somalia ,
                                                            'y_orders_solomon': y_orders_solomon,
                                                            'y_orders_slovenia': y_orders_slovenia,
                                                            'y_orders_slovakia': y_orders_slovakia,
                                                            'y_orders_singapore': y_orders_singapore,
                                                            'y_orders_sierra': y_orders_sierra,
                                                            'y_orders_serbia': y_orders_serbia,
                                                            'y_orders_senegal': y_orders_senegal,
                                                            'y_orders_san': y_orders_san,
                                                            'y_orders_rwanda': y_orders_rwanda,
                                                            'y_orders_russia': y_orders_russia,
                                                            'y_orders_romania': y_orders_romania,
                                                            'y_orders_qatar': y_orders_qatar,
                                                            'y_orders_portugal': y_orders_portugal,
                                                            'y_orders_poland': y_orders_poland,
                                                            'y_orders_philippines': y_orders_philippines,
                                                            'y_orders_peru': y_orders_peru,
                                                            'y_orders_paraguay': y_orders_paraguay,
                                                            'y_orders_pakistan': y_orders_pakistan,
                                                            'y_orders_oman': y_orders_oman,
                                                            'y_orders_norway': y_orders_norway,
                                                            'y_orders_niue': y_orders_niue,
                                                            'y_orders_niger':  y_orders_niger,
                                                            'y_orders_nicaragua': y_orders_nicaragua,
                                                            'y_orders_newz': y_orders_newz,
                                                            'y_orders_netherlands': y_orders_netherlands,
                                                            'y_orders_nepal': y_orders_nepal,
                                                            'y_orders_namibia': y_orders_namibia,
                                                            'y_orders_mozambique': y_orders_mozambique,
                                                            'y_orders_morocco': y_orders_morocco,
                                                            'y_orders_montenegro': y_orders_montenegro,
                                                            'y_orders_mongolia': y_orders_mongolia,
                                                            'y_orders_moldova': y_orders_moldova,
                                                            'y_orders_mexico': y_orders_mexico,
                                                            'y_orders_mauritius': y_orders_mauritius,
                                                            'y_orders_mauritania': y_orders_mauritania,
                                                            'y_orders_malta': y_orders_malta,
                                                            'y_orders_mali': y_orders_mali,
                                                            'y_orders_malaysia': y_orders_malaysia,
                                                            'y_orders_malawi': y_orders_malawi,
                                                            'y_orders_madagascar': y_orders_madagascar,
                                                            'y_orders_luxembourg': y_orders_luxembourg,
                                                            'y_orders_lithuania': y_orders_lithuania,
                                                            'y_orders_liechtenstein': y_orders_liechtenstein,
                                                            'y_orders_libya': y_orders_libya,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_lesotho': y_orders_lesotho,
                                                            'y_orders_lebanon': y_orders_lebanon,
                                                            'y_orders_latvia': y_orders_latvia,
                                                            'y_orders_kuwait': y_orders_kuwait,
                                                            'y_orders_korea': y_orders_korea,
                                                            'y_orders_kenya': y_orders_kenya,
                                                            'y_orders_kazakhstan': y_orders_kazakhstan,
                                                            'y_orders_jordan': y_orders_jordan,
                                                            'y_orders_japan': y_orders_japan,
                                                            'y_orders_jamaica': y_orders_jamaica,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_israel': y_orders_israel,
                                                            'y_orders_ireland': y_orders_ireland,
                                                            'y_orders_iran': y_orders_iran,
                                                            'y_orders_iraq': y_orders_iraq,
                                                            'y_orders_indonesia': y_orders_indonesia,
                                                            'y_orders_india': y_orders_india,
                                                            'y_orders_iceland': y_orders_iceland,
                                                            'y_orders_hungary': y_orders_hungary,
                                                            'y_orders_hong': y_orders_hong,
                                                            'y_orders_honduras': y_orders_honduras,
                                                            'y_orders_haiti': y_orders_haiti,
                                                            'y_orders_guineab': y_orders_guineab,
                                                            'y_orders_guinea': y_orders_guinea,
                                                            'y_orders_guatemala': y_orders_guatemala,
                                                            'y_orders_greenland': y_orders_greenland,
                                                            'y_orders_greece': y_orders_greece,
                                                            'y_orders_gibraltar': y_orders_gibraltar,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_georgia': y_orders_georgia,
                                                            'y_orders_gambia': y_orders_gambia,
                                                            'y_orders_gabon': y_orders_gabon,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_finland': y_orders_finland,
                                                            'y_orders_faroe': y_orders_faroe,
                                                            'y_orders_ethiopia': y_orders_ethiopia,
                                                            'y_orders_estonia': y_orders_estonia,
                                                            'y_orders_eritrea': y_orders_eritrea,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_els': y_orders_els,
                                                            'y_orders_egypt': y_orders_egypt,
                                                            'y_orders_ecuador': y_orders_ecuador,
                                                            'y_orders_denmark': y_orders_denmark,
                                                            'y_orders_czech': y_orders_czech,
                                                            'y_orders_cyprus': y_orders_cyprus,
                                                            'y_orders_cuba': y_orders_cuba,
                                                            'y_orders_croatia': y_orders_croatia,
                                                            'y_orders_ivory': y_orders_ivory,
                                                            'y_orders_costa': y_orders_costa,
                                                            'y_orders_congo': y_orders_congo,
                                                            'y_orders_colombia': y_orders_colombia,
                                                            'y_orders_christmas': y_orders_christmas,
                                                            'y_orders_china': y_orders_china,
                                                            'y_orders_chile': y_orders_chile,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_chad': y_orders_chad,
                                                            'y_orders_central': y_orders_central,
                                                            'y_orders_cape': y_orders_cape,
                                                            'y_orders_cameroo': y_orders_cameroo,
                                                            'y_orders_burundi': y_orders_burundi,
                                                            'y_orders_burkina': y_orders_burkina,
                                                            'y_orders_bulgaria': y_orders_bulgaria,
                                                            'y_orders_brazil': y_orders_brazil,
                                                            'y_orders_botswana': y_orders_botswana,
                                                            'y_orders_bosnia': y_orders_bosnia,
                                                            'y_orders_bolivia': y_orders_bolivia,
                                                            'y_orders_benin': y_orders_benin,
                                                            'y_orders_belgium': y_orders_belgium,
                                                            'y_orders_belarus': y_orders_belarus,
                                                            'y_orders_barbados': y_orders_barbados,
                                                            'y_orders_bangladesh': y_orders_bangladesh,
                                                            'y_orders_bahrain': y_orders_bahrain,
                                                            'y_orders_bahamas': y_orders_bahamas,
                                                            'y_orders_azerbaija': y_orders_azerbaija,
                                                            'y_orders_austria': y_orders_austria,
                                                            'y_orders_australi': y_orders_australi,
                                                            'y_orders_armenia': y_orders_armenia,
                                                            'y_orders_argentina': y_orders_argentina,
                                                            'y_orders_angola': y_orders_angola,
                                                            'y_orders_algeria': y_orders_algeria,
                                                            'y_orders_albania': y_orders_albania,
                                                            'y_orders_afghanistan': y_orders_afghanistan,
                                                            'is_entry': is_entry,
                                                            'is_lagos': is_lagos,
                                                            'is_daily': is_daily,
                                                            'product_value_total': product_value_total,
                                                            'y_orders_abia': y_orders_abia,
                                                            'y_orders_adamawa': y_orders_adamawa,
                                                            'y_orders_anambra': y_orders_anambra,
                                                            'y_orders_akwa_ibom': y_orders_akwa_ibom,
                                                            'y_orders_bauchi': y_orders_bauchi,
                                                            'y_orders_bayelsa': y_orders_bayelsa,
                                                            'y_orders_benue': y_orders_benue,
                                                            'y_orders_borno': y_orders_borno,
                                                            'y_orders_cross_river': y_orders_cross_river,
                                                            'y_orders_delta': y_orders_delta,
                                                            'y_orders_ebonyi': y_orders_ebonyi,
                                                            'y_orders_enugu': y_orders_enugu,
                                                            'y_orders_edo': y_orders_edo,
                                                            'y_orders_ekiti': y_orders_ekiti,
                                                            'y_orders_gombe': y_orders_gombe,
                                                            'y_orders_imo': y_orders_imo,
                                                            'y_orders_jigawa': y_orders_jigawa,
                                                            'y_orders_kaduna': y_orders_kaduna,
                                                            'y_orders_kano': y_orders_kano,
                                                            'y_orders_katsina': y_orders_katsina,
                                                            'y_orders_kebbi': y_orders_kebbi,
                                                            'y_orders_kogi': y_orders_kogi,
                                                            'y_orders_kwara': y_orders_kwara,
                                                            'y_orders_lagos': y_orders_lagos,
                                                            'y_orders_nasarawa': y_orders_nasarawa,
                                                            'y_orders_niger': y_orders_niger,
                                                            'y_orders_ogun': y_orders_ogun,
                                                            'y_orders_ondo': y_orders_ondo,
                                                            'y_orders_osun': y_orders_osun,
                                                            'y_orders_oyo': y_orders_oyo,
                                                            'y_orders_plateau': y_orders_plateau,
                                                            'y_orders_rivers': y_orders_rivers,
                                                            'y_orders_sokoto': y_orders_sokoto,
                                                            'y_orders_taraba': y_orders_taraba,
                                                            'y_orders_yobe': y_orders_yobe,
                                                            'y_orders_zamfara': y_orders_zamfara,
                                                            'y_orders_abuja': y_orders_abuja,
                                                            'y_orders_spain': y_orders_spain,
                                                            'y_orders_usa': y_orders_usa,
                                                            'y_orders_uk': y_orders_uk,
                                                            'y_orders_ghana': y_orders_ghana,
                                                            'y_orders_canada': y_orders_canada,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_saudi': y_orders_saudi,
                                                            'y_orders_south': y_orders_south,
                                                            'y_orders_switzerland': y_orders_switzerland,
                                                            'y_orders_turkey': y_orders_turkey,
                                                            'product_value_total_y': product_value_total_y,
                                                            })


@login_required
def view_pdf(request):
#class ClientDetail(DetailView):
    #model = Profile

    is_entry = request.user.groups.filter(name='entry').exists()
    is_lagos = request.user.groups.filter(name='lagos').exists()
    is_daily = request.user.groups.filter(name='daily').exists()
    categories = Category.objects.all()

    product_value_total = CustomerOrders.objects.filter( date_added=today).aggregate(Sum('product_value'))

    t_orders_Jakande = CustomerOrders.objects.filter( state='Jakande', date_added=today).aggregate(Sum('product_value'))
    t_orders_Sangotedo = CustomerOrders.objects.filter( state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    t_orders_Eleko = CustomerOrders.objects.filter( state='Eleko', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ajah = CustomerOrders.objects.filter( state='Ajah', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ogba = CustomerOrders.objects.filter( state='Ogba', date_added=today).aggregate(Sum('product_value'))
    t_orders_Aguda = CustomerOrders.objects.filter( state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ketu = CustomerOrders.objects.filter( state='Ketu', date_added=today).aggregate(Sum('product_value'))
    t_orders_VI = CustomerOrders.objects.filter( state='VI', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikotun = CustomerOrders.objects.filter( state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    t_orders_Oshodi = CustomerOrders.objects.filter( state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    t_orders_Ikeja = CustomerOrders.objects.filter( state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    t_orders_Lekki = CustomerOrders.objects.filter( state='Lekki', date_added=today).aggregate(Sum('product_value'))
    t_orders_Apapa = CustomerOrders.objects.filter( state='Apapa', date_added=today).aggregate(Sum('product_value'))


    t_orders_abia = CustomerOrders.objects.filter( state='abia', date_added=today).aggregate(Sum('product_value'))
    t_orders_adamawa = CustomerOrders.objects.filter( state='adamawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_anambra = CustomerOrders.objects.filter( state='anambra', date_added=today).aggregate(Sum('product_value'))
    t_orders_akwa_ibom = CustomerOrders.objects.filter( state='akwa-ibom', date_added=today).aggregate(Sum('product_value'))
    t_orders_bauchi = CustomerOrders.objects.filter( state='bauchi', date_added=today).aggregate(Sum('product_value'))
    t_orders_bayelsa = CustomerOrders.objects.filter( state='bayelsa', date_added=today).aggregate(Sum('product_value'))
    t_orders_benue = CustomerOrders.objects.filter( state='benue', date_added=today).aggregate(Sum('product_value'))
    t_orders_borno = CustomerOrders.objects.filter( state='borno', date_added=today).aggregate(Sum('product_value'))
    t_orders_cross_river = CustomerOrders.objects.filter( state='cross-river', date_added=today).aggregate(Sum('product_value'))
    t_orders_delta = CustomerOrders.objects.filter( state='delta', date_added=today).aggregate(Sum('product_value'))
    t_orders_ebonyi = CustomerOrders.objects.filter( state='ebonyi', date_added=today).aggregate(Sum('product_value'))
    t_orders_enugu = CustomerOrders.objects.filter( state='enugu', date_added=today).aggregate(Sum('product_value'))
    t_orders_edo = CustomerOrders.objects.filter( state='edo', date_added=today).aggregate(Sum('product_value'))
    t_orders_ekiti = CustomerOrders.objects.filter( state='ekiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_gombe = CustomerOrders.objects.filter( state='gombe', date_added=today).aggregate(Sum('product_value'))
    t_orders_imo = CustomerOrders.objects.filter( state='imo', date_added=today).aggregate(Sum('product_value'))
    t_orders_jigawa = CustomerOrders.objects.filter( state='jigawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_kaduna = CustomerOrders.objects.filter( state='kaduna', date_added=today).aggregate(Sum('product_value'))
    t_orders_kano = CustomerOrders.objects.filter( state='kano', date_added=today).aggregate(Sum('product_value'))
    t_orders_katsina = CustomerOrders.objects.filter( state='katsina', date_added=today).aggregate(Sum('product_value'))
    t_orders_kebbi = CustomerOrders.objects.filter( state='kebbi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kogi = CustomerOrders.objects.filter( state='kogi', date_added=today).aggregate(Sum('product_value'))
    t_orders_kwara = CustomerOrders.objects.filter( state='kwara', date_added=today).aggregate(Sum('product_value'))
    t_orders_lagos = CustomerOrders.objects.filter( state='lagos', date_added=today).aggregate(Sum('product_value'))
    t_orders_nasarawa = CustomerOrders.objects.filter( state='nasarawa', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter( state='niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_ogun = CustomerOrders.objects.filter( state='ogun', date_added=today).aggregate(Sum('product_value'))
    t_orders_ondo = CustomerOrders.objects.filter( state='ondo', date_added=today).aggregate(Sum('product_value'))
    t_orders_osun = CustomerOrders.objects.filter( state='osun', date_added=today).aggregate(Sum('product_value'))
    t_orders_oyo = CustomerOrders.objects.filter( state='oyo', date_added=today).aggregate(Sum('product_value'))
    t_orders_plateau = CustomerOrders.objects.filter( state='plateau', date_added=today).aggregate(Sum('product_value'))
    t_orders_rivers = CustomerOrders.objects.filter( state='rivers', date_added=today).aggregate(Sum('product_value'))
    t_orders_sokoto = CustomerOrders.objects.filter( state='sokoto', date_added=today).aggregate(Sum('product_value'))
    t_orders_taraba = CustomerOrders.objects.filter( state='taraba', date_added=today).aggregate(Sum('product_value'))
    t_orders_yobe = CustomerOrders.objects.filter( state='yobe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zamfara= CustomerOrders.objects.filter( state='zamfara', date_added=today).aggregate(Sum('product_value'))
    t_orders_abuja = CustomerOrders.objects.filter( state='abuja', date_added=today).aggregate(Sum('product_value'))
    t_orders_spain = CustomerOrders.objects.filter( state='spain', date_added=today).aggregate(Sum('product_value'))
    t_orders_usa = CustomerOrders.objects.filter( state='USA', date_added=today).aggregate(Sum('product_value'))
    t_orders_uk = CustomerOrders.objects.filter( state='UK', date_added=today).aggregate(Sum('product_value'))
    t_orders_ghana = CustomerOrders.objects.filter( state='Ghana', date_added=today).aggregate(Sum('product_value'))
    t_orders_canada = CustomerOrders.objects.filter( state='canada', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter( state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_saudi = CustomerOrders.objects.filter( state='Saudi Arabia', date_added=today).aggregate(Sum('product_value'))
    t_orders_south = CustomerOrders.objects.filter( state='South Africa', date_added=today).aggregate(Sum('product_value'))
    t_orders_switzerland = CustomerOrders.objects.filter( state='Switzerland', date_added=today).aggregate(Sum('product_value'))
    t_orders_turkey = CustomerOrders.objects.filter( state='Turkey', date_added=today).aggregate(Sum('product_value'))

    t_orders_zimbabwe = CustomerOrders.objects.filter( state='Zimbabwe', date_added=today).aggregate(Sum('product_value'))
    t_orders_zambia = CustomerOrders.objects.filter( state='Zambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_yemen = CustomerOrders.objects.filter( state='Yemen', date_added=today).aggregate(Sum('product_value'))
    t_orders_venezuela = CustomerOrders.objects.filter( state='Venezuela', date_added=today).aggregate(Sum('product_value'))
    t_orders_uzbekistan = CustomerOrders.objects.filter( state='Uzbekistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_uruguay = CustomerOrders.objects.filter( state='Uruguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_uae = CustomerOrders.objects.filter( state='United Arab Emirates', date_added=today).aggregate(Sum('product_value'))
    t_orders_ukraine = CustomerOrders.objects.filter( state='Ukraine', date_added=today).aggregate(Sum('product_value'))
    t_orders_uganda = CustomerOrders.objects.filter( state='Uganda', date_added=today).aggregate(Sum('product_value'))
    t_orders_tunisia = CustomerOrders.objects.filter( state='Tunisia', date_added=today).aggregate(Sum('product_value'))
    t_orders_trinidad = CustomerOrders.objects.filter( state='Trinidad and Tobago', date_added=today).aggregate(Sum('product_value'))
    t_orders_togo = CustomerOrders.objects.filter( state='Togo', date_added=today).aggregate(Sum('product_value'))
    t_orders_thailand = CustomerOrders.objects.filter( state='Thailand', date_added=today).aggregate(Sum('product_value'))
    t_orders_tanzania = CustomerOrders.objects.filter( state='Tanzania', date_added=today).aggregate(Sum('product_value'))
    t_orders_taiwan = CustomerOrders.objects.filter( state='Taiwan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sweden = CustomerOrders.objects.filter( state='Sweden', date_added=today).aggregate(Sum('product_value'))
    t_orders_swaziland = CustomerOrders.objects.filter( state='Swaziland', date_added=today).aggregate(Sum('product_value'))
    t_orders_sudan = CustomerOrders.objects.filter( state='Sudan', date_added=today).aggregate(Sum('product_value'))
    t_orders_sri = CustomerOrders.objects.filter( state='Sri Lanka', date_added=today).aggregate(Sum('product_value'))
    t_orders_somalia = CustomerOrders.objects.filter( state='Somalia', date_added=today).aggregate(Sum('product_value'))
    t_orders_solomon = CustomerOrders.objects.filter( state='Solomon Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovenia = CustomerOrders.objects.filter( state='Slovenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_slovakia = CustomerOrders.objects.filter( state='Slovakia', date_added=today).aggregate(Sum('product_value'))
    t_orders_singapore = CustomerOrders.objects.filter( state='Singapore', date_added=today).aggregate(Sum('product_value'))
    t_orders_sierra = CustomerOrders.objects.filter( state='Sierra Leone', date_added=today).aggregate(Sum('product_value'))
    t_orders_serbia = CustomerOrders.objects.filter( state='Serbia', date_added=today).aggregate(Sum('product_value'))
    t_orders_senegal = CustomerOrders.objects.filter( state='Senegal', date_added=today).aggregate(Sum('product_value'))
    t_orders_san = CustomerOrders.objects.filter( state='San Marino', date_added=today).aggregate(Sum('product_value'))
    t_orders_rwanda = CustomerOrders.objects.filter( state='Rwanda', date_added=today).aggregate(Sum('product_value'))
    t_orders_russia = CustomerOrders.objects.filter( state='Russian Federation', date_added=today).aggregate(Sum('product_value'))
    t_orders_romania = CustomerOrders.objects.filter( state='Romania', date_added=today).aggregate(Sum('product_value'))
    t_orders_qatar = CustomerOrders.objects.filter( state='Qatar', date_added=today).aggregate(Sum('product_value'))
    t_orders_portugal = CustomerOrders.objects.filter( state='Portugal', date_added=today).aggregate(Sum('product_value'))
    t_orders_poland = CustomerOrders.objects.filter( state='Poland', date_added=today).aggregate(Sum('product_value'))
    t_orders_philippines = CustomerOrders.objects.filter( state='Philippines', date_added=today).aggregate(Sum('product_value'))
    t_orders_peru = CustomerOrders.objects.filter( state='Peru', date_added=today).aggregate(Sum('product_value'))
    t_orders_paraguay = CustomerOrders.objects.filter( state='Paraguay', date_added=today).aggregate(Sum('product_value'))
    t_orders_pakistan = CustomerOrders.objects.filter( state='Pakistan', date_added=today).aggregate(Sum('product_value'))
    t_orders_oman = CustomerOrders.objects.filter( state='Oman', date_added=today).aggregate(Sum('product_value'))
    t_orders_norway = CustomerOrders.objects.filter( state='Norway', date_added=today).aggregate(Sum('product_value'))
    t_orders_niue = CustomerOrders.objects.filter( state='Niue', date_added=today).aggregate(Sum('product_value'))
    t_orders_niger = CustomerOrders.objects.filter( state='Niger', date_added=today).aggregate(Sum('product_value'))
    t_orders_nicaragua = CustomerOrders.objects.filter( state='Nicaragua', date_added=today).aggregate(Sum('product_value'))
    t_orders_newz = CustomerOrders.objects.filter( state='New Zealand', date_added=today).aggregate(Sum('product_value'))
    t_orders_netherlands = CustomerOrders.objects.filter( state='Netherlands', date_added=today).aggregate(Sum('product_value'))
    t_orders_nepal = CustomerOrders.objects.filter( state='Nepal', date_added=today).aggregate(Sum('product_value'))
    t_orders_namibia = CustomerOrders.objects.filter( state='Namibia', date_added=today).aggregate(Sum('product_value'))
    t_orders_mozambique = CustomerOrders.objects.filter( state='Mozambique', date_added=today).aggregate(Sum('product_value'))
    t_orders_morocco = CustomerOrders.objects.filter( state='Morocco', date_added=today).aggregate(Sum('product_value'))
    t_orders_montenegro = CustomerOrders.objects.filter( state='Montenegro', date_added=today).aggregate(Sum('product_value'))
    t_orders_mongolia = CustomerOrders.objects.filter( state='Mongolia', date_added=today).aggregate(Sum('product_value'))
    t_orders_moldova = CustomerOrders.objects.filter( state='Moldova', date_added=today).aggregate(Sum('product_value'))
    t_orders_mexico = CustomerOrders.objects.filter( state='Mexico', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritius = CustomerOrders.objects.filter( state='Mauritius', date_added=today).aggregate(Sum('product_value'))
    t_orders_mauritania = CustomerOrders.objects.filter( state='Mauritania', date_added=today).aggregate(Sum('product_value'))
    t_orders_malta = CustomerOrders.objects.filter( state='Malta', date_added=today).aggregate(Sum('product_value'))
    t_orders_mali = CustomerOrders.objects.filter( state='Mali', date_added=today).aggregate(Sum('product_value'))
    t_orders_malaysia = CustomerOrders.objects.filter( state='Malaysia', date_added=today).aggregate(Sum('product_value'))
    t_orders_malawi = CustomerOrders.objects.filter( state='Malawi', date_added=today).aggregate(Sum('product_value'))
    t_orders_madagascar = CustomerOrders.objects.filter( state='Madagascar', date_added=today).aggregate(Sum('product_value'))
    t_orders_luxembourg = CustomerOrders.objects.filter( state='Luxembourg', date_added=today).aggregate(Sum('product_value'))
    t_orders_lithuania = CustomerOrders.objects.filter( state='Lithuania', date_added=today).aggregate(Sum('product_value'))
    t_orders_liechtenstein = CustomerOrders.objects.filter( state='Liechtenstein', date_added=today).aggregate(Sum('product_value'))
    t_orders_libya = CustomerOrders.objects.filter( state='Libya', date_added=today).aggregate(Sum('product_value'))
    t_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=today).aggregate(Sum('product_value'))
    t_orders_lesotho = CustomerOrders.objects.filter( state='Lesotho', date_added=today).aggregate(Sum('product_value'))
    t_orders_lebanon = CustomerOrders.objects.filter( state='Lebanon', date_added=today).aggregate(Sum('product_value'))
    t_orders_latvia = CustomerOrders.objects.filter( state='Latvia', date_added=today).aggregate(Sum('product_value'))
    t_orders_kuwait = CustomerOrders.objects.filter( state='Kuwait', date_added=today).aggregate(Sum('product_value'))
    t_orders_korea = CustomerOrders.objects.filter( state='Korea', date_added=today).aggregate(Sum('product_value'))
    t_orders_kenya = CustomerOrders.objects.filter( state='Kenya', date_added=today).aggregate(Sum('product_value'))
    t_orders_kazakhstan = CustomerOrders.objects.filter( state='Kazakhstan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jordan = CustomerOrders.objects.filter( state='Jordan', date_added=today).aggregate(Sum('product_value'))
    t_orders_japan = CustomerOrders.objects.filter( state='Japan', date_added=today).aggregate(Sum('product_value'))
    t_orders_jamaica = CustomerOrders.objects.filter( state='Jamaica', date_added=today).aggregate(Sum('product_value'))
    t_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=today).aggregate(Sum('product_value'))
    t_orders_israel = CustomerOrders.objects.filter( state='Israel', date_added=today).aggregate(Sum('product_value'))
    t_orders_ireland = CustomerOrders.objects.filter( state='Ireland', date_added=today).aggregate(Sum('product_value'))
    t_orders_iran = CustomerOrders.objects.filter( state='Iran', date_added=today).aggregate(Sum('product_value'))
    t_orders_iraq = CustomerOrders.objects.filter( state='Iraq', date_added=today).aggregate(Sum('product_value'))
    t_orders_indonesia = CustomerOrders.objects.filter( state='Indonesia', date_added=today).aggregate(Sum('product_value'))
    t_orders_india = CustomerOrders.objects.filter( state='India', date_added=today).aggregate(Sum('product_value'))
    t_orders_iceland = CustomerOrders.objects.filter( state='Iceland', date_added=today).aggregate(Sum('product_value'))
    t_orders_hungary = CustomerOrders.objects.filter( state='Hungary', date_added=today).aggregate(Sum('product_value'))
    t_orders_hong = CustomerOrders.objects.filter( state='Hong Kong', date_added=today).aggregate(Sum('product_value'))
    t_orders_honduras = CustomerOrders.objects.filter( state='Honduras', date_added=today).aggregate(Sum('product_value'))
    t_orders_haiti = CustomerOrders.objects.filter( state='Haiti', date_added=today).aggregate(Sum('product_value'))
    t_orders_guineab = CustomerOrders.objects.filter( state='Guinea-Bissau', date_added=today).aggregate(Sum('product_value'))
    t_orders_guinea = CustomerOrders.objects.filter( state='Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_guatemala = CustomerOrders.objects.filter( state='Guatemala', date_added=today).aggregate(Sum('product_value'))
    t_orders_greenland = CustomerOrders.objects.filter( state='Greenland', date_added=today).aggregate(Sum('product_value'))
    t_orders_greece = CustomerOrders.objects.filter( state='Greece', date_added=today).aggregate(Sum('product_value'))
    t_orders_gibraltar = CustomerOrders.objects.filter( state='Gibraltar', date_added=today).aggregate(Sum('product_value'))
    t_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=today).aggregate(Sum('product_value'))
    t_orders_georgia = CustomerOrders.objects.filter( state='Georgia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gambia = CustomerOrders.objects.filter( state='Gambia', date_added=today).aggregate(Sum('product_value'))
    t_orders_gabon = CustomerOrders.objects.filter( state='Gabon', date_added=today).aggregate(Sum('product_value'))
    t_orders_france = CustomerOrders.objects.filter( state='France', date_added=today).aggregate(Sum('product_value'))
    t_orders_finland = CustomerOrders.objects.filter( state='Finland', date_added=today).aggregate(Sum('product_value'))
    t_orders_faroe = CustomerOrders.objects.filter( state='Faroe Islands', date_added=today).aggregate(Sum('product_value'))
    t_orders_ethiopia = CustomerOrders.objects.filter( state='Ethiopia', date_added=today).aggregate(Sum('product_value'))
    t_orders_estonia = CustomerOrders.objects.filter( state='Estonia', date_added=today).aggregate(Sum('product_value'))
    t_orders_eritrea = CustomerOrders.objects.filter( state='Eritrea', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_els = CustomerOrders.objects.filter( state='El Salvador', date_added=today).aggregate(Sum('product_value'))
    t_orders_egypt = CustomerOrders.objects.filter( state='Egypt', date_added=today).aggregate(Sum('product_value'))
    t_orders_ecuador = CustomerOrders.objects.filter( state='Ecuador', date_added=today).aggregate(Sum('product_value'))
    t_orders_denmark = CustomerOrders.objects.filter( state='Denmark', date_added=today).aggregate(Sum('product_value'))
    t_orders_czech = CustomerOrders.objects.filter( state='Czech Republic', date_added=today).aggregate(Sum('product_value'))
    t_orders_cyprus = CustomerOrders.objects.filter( state='Cyprus', date_added=today).aggregate(Sum('product_value'))
    t_orders_cuba = CustomerOrders.objects.filter( state='Cuba', date_added=today).aggregate(Sum('product_value'))
    t_orders_croatia = CustomerOrders.objects.filter( state='Croatia', date_added=today).aggregate(Sum('product_value'))
    t_orders_ivory = CustomerOrders.objects.filter( state='Ivory Coast', date_added=today).aggregate(Sum('product_value'))
    t_orders_costa = CustomerOrders.objects.filter( state='Costa Rica', date_added=today).aggregate(Sum('product_value'))
    t_orders_congo = CustomerOrders.objects.filter( state='Congo', date_added=today).aggregate(Sum('product_value'))
    t_orders_colombia = CustomerOrders.objects.filter( state='Colombia', date_added=today).aggregate(Sum('product_value'))
    t_orders_christmas = CustomerOrders.objects.filter( state='Christmas Island', date_added=today).aggregate(Sum('product_value'))
    t_orders_china = CustomerOrders.objects.filter( state='China', date_added=today).aggregate(Sum('product_value'))
    t_orders_chile = CustomerOrders.objects.filter( state='Chile', date_added=today).aggregate(Sum('product_value'))
    t_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=today).aggregate(Sum('product_value'))
    t_orders_chad = CustomerOrders.objects.filter( state='Chad', date_added=today).aggregate(Sum('product_value'))
    t_orders_central = CustomerOrders.objects.filter( state='Central African Republi', date_added=today).aggregate(Sum('product_value'))
    t_orders_cape = CustomerOrders.objects.filter( state='Cape Verde', date_added=today).aggregate(Sum('product_value'))
    t_orders_cameroo = CustomerOrders.objects.filter( state='Cameroo', date_added=today).aggregate(Sum('product_value'))
    t_orders_burundi = CustomerOrders.objects.filter( state='Burundi', date_added=today).aggregate(Sum('product_value'))
    t_orders_burkina = CustomerOrders.objects.filter( state='Burkina Faso', date_added=today).aggregate(Sum('product_value'))
    t_orders_bulgaria = CustomerOrders.objects.filter( state='Bulgaria', date_added=today).aggregate(Sum('product_value'))
    t_orders_brazil = CustomerOrders.objects.filter( state='Brazil', date_added=today).aggregate(Sum('product_value'))
    t_orders_botswana = CustomerOrders.objects.filter( state='Botswana', date_added=today).aggregate(Sum('product_value'))
    t_orders_bosnia = CustomerOrders.objects.filter( state='Bosnia and Herzegovina', date_added=today).aggregate(Sum('product_value'))
    t_orders_bolivia = CustomerOrders.objects.filter( state='Bolivia', date_added=today).aggregate(Sum('product_value'))
    t_orders_benin = CustomerOrders.objects.filter( state='Benin', date_added=today).aggregate(Sum('product_value'))
    t_orders_belgium = CustomerOrders.objects.filter( state='Belgium', date_added=today).aggregate(Sum('product_value'))
    t_orders_belarus = CustomerOrders.objects.filter( state='Belarus', date_added=today).aggregate(Sum('product_value'))
    t_orders_barbados = CustomerOrders.objects.filter( state='Barbados', date_added=today).aggregate(Sum('product_value'))
    t_orders_bangladesh = CustomerOrders.objects.filter( state='Bangladesh', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahrain = CustomerOrders.objects.filter( state='Bahrain', date_added=today).aggregate(Sum('product_value'))
    t_orders_bahamas = CustomerOrders.objects.filter( state='Bahamas', date_added=today).aggregate(Sum('product_value'))
    t_orders_azerbaija = CustomerOrders.objects.filter( state='Azerbaija', date_added=today).aggregate(Sum('product_value'))
    t_orders_austria = CustomerOrders.objects.filter( state='Austria', date_added=today).aggregate(Sum('product_value'))
    t_orders_australi = CustomerOrders.objects.filter( state='Australi', date_added=today).aggregate(Sum('product_value'))
    t_orders_armenia = CustomerOrders.objects.filter( state='Armenia', date_added=today).aggregate(Sum('product_value'))
    t_orders_argentina = CustomerOrders.objects.filter( state='Argentina', date_added=today).aggregate(Sum('product_value'))
    t_orders_angola = CustomerOrders.objects.filter( state='Angola', date_added=today).aggregate(Sum('product_value'))
    t_orders_algeria = CustomerOrders.objects.filter( state='Algeria', date_added=today).aggregate(Sum('product_value'))
    t_orders_albania = CustomerOrders.objects.filter( state='Albania', date_added=today).aggregate(Sum('product_value'))
    t_orders_afghanistan = CustomerOrders.objects.filter( state='Afghanistan', date_added=today).aggregate(Sum('product_value'))


    product_value_total_y = CustomerOrders.objects.filter( date_added=yesterday).aggregate(Sum('product_value'))

    y_orders_Jakande = CustomerOrders.objects.filter( state='Jakande', date_added=today).aggregate(Sum('product_value'))
    y_orders_Sangotedo = CustomerOrders.objects.filter( state='Sangotedo', date_added=today).aggregate(Sum('product_value'))
    y_orders_Eleko = CustomerOrders.objects.filter( state='Eleko', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ajah = CustomerOrders.objects.filter( state='Ajah', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ogba = CustomerOrders.objects.filter( state='Ogba', date_added=today).aggregate(Sum('product_value'))
    y_orders_Aguda = CustomerOrders.objects.filter( state='Aguda/Surulere', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ketu = CustomerOrders.objects.filter( state='Ketu', date_added=today).aggregate(Sum('product_value'))
    y_orders_VI = CustomerOrders.objects.filter( state='VI', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikotun = CustomerOrders.objects.filter( state='Ikotun', date_added=today).aggregate(Sum('product_value'))
    y_orders_Oshodi = CustomerOrders.objects.filter( state='Oshodi', date_added=today).aggregate(Sum('product_value'))
    y_orders_Ikeja = CustomerOrders.objects.filter( state='Ikeja', date_added=today).aggregate(Sum('product_value'))
    y_orders_Lekki = CustomerOrders.objects.filter( state='Lekki', date_added=today).aggregate(Sum('product_value'))
    y_orders_Apapa = CustomerOrders.objects.filter( state='Apapa', date_added=today).aggregate(Sum('product_value'))

    y_orders_abia = CustomerOrders.objects.filter( state='abia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_adamawa = CustomerOrders.objects.filter( state='adamawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_anambra = CustomerOrders.objects.filter( state='anambra', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_akwa_ibom = CustomerOrders.objects.filter( state='akwa-ibom', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bauchi = CustomerOrders.objects.filter( state='bauchi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bayelsa = CustomerOrders.objects.filter( state='bayelsa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benue = CustomerOrders.objects.filter( state='benue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_borno = CustomerOrders.objects.filter( state='borno', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cross_river = CustomerOrders.objects.filter( state='cross-river', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_delta = CustomerOrders.objects.filter( state='delta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ebonyi = CustomerOrders.objects.filter( state='ebonyi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_enugu = CustomerOrders.objects.filter( state='enugu', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_edo = CustomerOrders.objects.filter( state='edo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ekiti = CustomerOrders.objects.filter( state='ekiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gombe = CustomerOrders.objects.filter( state='gombe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_imo = CustomerOrders.objects.filter( state='imo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jigawa = CustomerOrders.objects.filter( state='jigawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kaduna = CustomerOrders.objects.filter( state='kaduna', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kano = CustomerOrders.objects.filter( state='kano', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_katsina = CustomerOrders.objects.filter( state='katsina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kebbi = CustomerOrders.objects.filter( state='kebbi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kogi = CustomerOrders.objects.filter( state='kogi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kwara = CustomerOrders.objects.filter( state='kwara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lagos = CustomerOrders.objects.filter( state='lagos', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nasarawa = CustomerOrders.objects.filter( state='nasarawa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter( state='niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ogun = CustomerOrders.objects.filter( state='ogun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ondo = CustomerOrders.objects.filter( state='ondo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_osun = CustomerOrders.objects.filter( state='osun', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oyo = CustomerOrders.objects.filter( state='oyo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_plateau = CustomerOrders.objects.filter( state='plateau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rivers = CustomerOrders.objects.filter( state='rivers', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sokoto = CustomerOrders.objects.filter( state='sokoto', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taraba = CustomerOrders.objects.filter( state='taraba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yobe = CustomerOrders.objects.filter( state='yobe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zamfara= CustomerOrders.objects.filter( state='zamfara', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_abuja = CustomerOrders.objects.filter( state='abuja', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_spain = CustomerOrders.objects.filter( state='spain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_usa = CustomerOrders.objects.filter( state='USA', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uk = CustomerOrders.objects.filter( state='UK', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ghana = CustomerOrders.objects.filter( state='Ghana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_canada = CustomerOrders.objects.filter( state='canada', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter( state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_saudi = CustomerOrders.objects.filter( state='Saudi Arabia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_south = CustomerOrders.objects.filter( state='South Africa', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_switzerland = CustomerOrders.objects.filter( state='Switzerland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_turkey = CustomerOrders.objects.filter( state='Turkey', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zimbabwe = CustomerOrders.objects.filter( state='Zimbabwe', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_zambia = CustomerOrders.objects.filter( state='Zambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_yemen = CustomerOrders.objects.filter( state='Yemen', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_venezuela = CustomerOrders.objects.filter( state='Venezuela', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uzbekistan = CustomerOrders.objects.filter( state='Uzbekistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uruguay = CustomerOrders.objects.filter( state='Uruguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uae = CustomerOrders.objects.filter( state='United Arab Emirates', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ukraine = CustomerOrders.objects.filter( state='Ukraine', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_uganda = CustomerOrders.objects.filter( state='Uganda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tunisia = CustomerOrders.objects.filter( state='Tunisia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_trinidad = CustomerOrders.objects.filter( state='Trinidad and Tobago', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_togo = CustomerOrders.objects.filter( state='Togo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_thailand = CustomerOrders.objects.filter( state='Thailand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_tanzania = CustomerOrders.objects.filter( state='Tanzania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_taiwan = CustomerOrders.objects.filter( state='Taiwan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sweden = CustomerOrders.objects.filter( state='Sweden', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_swaziland = CustomerOrders.objects.filter( state='Swaziland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sudan = CustomerOrders.objects.filter( state='Sudan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sri = CustomerOrders.objects.filter( state='Sri Lanka', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_somalia = CustomerOrders.objects.filter( state='Somalia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_solomon = CustomerOrders.objects.filter( state='Solomon Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovenia = CustomerOrders.objects.filter( state='Slovenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_slovakia = CustomerOrders.objects.filter( state='Slovakia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_singapore = CustomerOrders.objects.filter( state='Singapore', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_sierra = CustomerOrders.objects.filter( state='Sierra Leone', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_serbia = CustomerOrders.objects.filter( state='Serbia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_senegal = CustomerOrders.objects.filter( state='Senegal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_san = CustomerOrders.objects.filter( state='San Marino', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_rwanda = CustomerOrders.objects.filter( state='Rwanda', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_russia = CustomerOrders.objects.filter( state='Russian Federation', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_romania = CustomerOrders.objects.filter( state='Romania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_qatar = CustomerOrders.objects.filter( state='Qatar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_portugal = CustomerOrders.objects.filter( state='Portugal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_poland = CustomerOrders.objects.filter( state='Poland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_philippines = CustomerOrders.objects.filter( state='Philippines', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_peru = CustomerOrders.objects.filter( state='Peru', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_paraguay = CustomerOrders.objects.filter( state='Paraguay', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_pakistan = CustomerOrders.objects.filter( state='Pakistan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_oman = CustomerOrders.objects.filter( state='Oman', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_norway = CustomerOrders.objects.filter( state='Norway', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niue = CustomerOrders.objects.filter( state='Niue', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_niger = CustomerOrders.objects.filter( state='Niger', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nicaragua = CustomerOrders.objects.filter( state='Nicaragua', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_newz = CustomerOrders.objects.filter( state='New Zealand', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_netherlands = CustomerOrders.objects.filter( state='Netherlands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_nepal = CustomerOrders.objects.filter( state='Nepal', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_namibia = CustomerOrders.objects.filter( state='Namibia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mozambique = CustomerOrders.objects.filter( state='Mozambique', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_morocco = CustomerOrders.objects.filter( state='Morocco', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_montenegro = CustomerOrders.objects.filter( state='Montenegro', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mongolia = CustomerOrders.objects.filter( state='Mongolia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_moldova = CustomerOrders.objects.filter( state='Moldova', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mexico = CustomerOrders.objects.filter( state='Mexico', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritius = CustomerOrders.objects.filter( state='Mauritius', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mauritania = CustomerOrders.objects.filter( state='Mauritania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malta = CustomerOrders.objects.filter( state='Malta', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_mali = CustomerOrders.objects.filter( state='Mali', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malaysia = CustomerOrders.objects.filter( state='Malaysia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_malawi = CustomerOrders.objects.filter( state='Malawi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_madagascar = CustomerOrders.objects.filter( state='Madagascar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_luxembourg = CustomerOrders.objects.filter( state='Luxembourg', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lithuania = CustomerOrders.objects.filter( state='Lithuania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liechtenstein = CustomerOrders.objects.filter( state='Liechtenstein', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_libya = CustomerOrders.objects.filter( state='Libya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_liberia = CustomerOrders.objects.filter( state='Liberia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lesotho = CustomerOrders.objects.filter( state='Lesotho', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_lebanon = CustomerOrders.objects.filter( state='Lebanon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_latvia = CustomerOrders.objects.filter( state='Latvia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kuwait = CustomerOrders.objects.filter( state='Kuwait', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_korea = CustomerOrders.objects.filter( state='Korea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kenya = CustomerOrders.objects.filter( state='Kenya', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_kazakhstan = CustomerOrders.objects.filter( state='Kazakhstan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jordan = CustomerOrders.objects.filter( state='Jordan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_japan = CustomerOrders.objects.filter( state='Japan', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_jamaica = CustomerOrders.objects.filter( state='Jamaica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_italy = CustomerOrders.objects.filter( state='Italy', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_israel = CustomerOrders.objects.filter( state='Israel', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ireland = CustomerOrders.objects.filter( state='Ireland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iran = CustomerOrders.objects.filter( state='Iran', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iraq = CustomerOrders.objects.filter( state='Iraq', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_indonesia = CustomerOrders.objects.filter( state='Indonesia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_india = CustomerOrders.objects.filter( state='India', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_iceland = CustomerOrders.objects.filter( state='Iceland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hungary = CustomerOrders.objects.filter( state='Hungary', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_hong = CustomerOrders.objects.filter( state='Hong Kong', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_honduras = CustomerOrders.objects.filter( state='Honduras', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_haiti = CustomerOrders.objects.filter( state='Haiti', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guineab = CustomerOrders.objects.filter( state='Guinea-Bissau', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guinea = CustomerOrders.objects.filter( state='Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_guatemala = CustomerOrders.objects.filter( state='Guatemala', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greenland = CustomerOrders.objects.filter( state='Greenland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_greece = CustomerOrders.objects.filter( state='Greece', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gibraltar = CustomerOrders.objects.filter( state='Gibraltar', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_germany = CustomerOrders.objects.filter( state='Germany', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_georgia = CustomerOrders.objects.filter( state='Georgia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gambia = CustomerOrders.objects.filter( state='Gambia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_gabon = CustomerOrders.objects.filter( state='Gabon', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_france = CustomerOrders.objects.filter( state='France', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_finland = CustomerOrders.objects.filter( state='Finland', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_faroe = CustomerOrders.objects.filter( state='Faroe Islands', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ethiopia = CustomerOrders.objects.filter( state='Ethiopia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_estonia = CustomerOrders.objects.filter( state='Estonia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_eritrea = CustomerOrders.objects.filter( state='Eritrea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_els = CustomerOrders.objects.filter( state='El Salvador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_egypt = CustomerOrders.objects.filter( state='Egypt', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ecuador = CustomerOrders.objects.filter( state='Ecuador', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_denmark = CustomerOrders.objects.filter( state='Denmark', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_czech = CustomerOrders.objects.filter( state='Czech Republic', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cyprus = CustomerOrders.objects.filter( state='Cyprus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cuba = CustomerOrders.objects.filter( state='Cuba', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_croatia = CustomerOrders.objects.filter( state='Croatia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_ivory = CustomerOrders.objects.filter( state='Ivory Coast', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_costa = CustomerOrders.objects.filter( state='Costa Rica', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_congo = CustomerOrders.objects.filter( state='Congo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_colombia = CustomerOrders.objects.filter( state='Colombia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_christmas = CustomerOrders.objects.filter( state='Christmas Island', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_china = CustomerOrders.objects.filter( state='China', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chile = CustomerOrders.objects.filter( state='Chile', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_equatorial = CustomerOrders.objects.filter( state='Equatorial Guinea', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_chad = CustomerOrders.objects.filter( state='Chad', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_central = CustomerOrders.objects.filter( state='Central African Republi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cape = CustomerOrders.objects.filter( state='Cape Verde', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_cameroo = CustomerOrders.objects.filter( state='Cameroo', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burundi = CustomerOrders.objects.filter( state='Burundi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_burkina = CustomerOrders.objects.filter( state='Burkina Faso', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bulgaria = CustomerOrders.objects.filter( state='Bulgaria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_brazil = CustomerOrders.objects.filter( state='Brazil', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_botswana = CustomerOrders.objects.filter( state='Botswana', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bosnia = CustomerOrders.objects.filter( state='Bosnia and Herzegovina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bolivia = CustomerOrders.objects.filter( state='Bolivia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_benin = CustomerOrders.objects.filter( state='Benin', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belgium = CustomerOrders.objects.filter( state='Belgium', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_belarus = CustomerOrders.objects.filter( state='Belarus', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_barbados = CustomerOrders.objects.filter( state='Barbados', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bangladesh = CustomerOrders.objects.filter( state='Bangladesh', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahrain = CustomerOrders.objects.filter( state='Bahrain', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_bahamas = CustomerOrders.objects.filter( state='Bahamas', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_azerbaija = CustomerOrders.objects.filter( state='Azerbaija', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_austria = CustomerOrders.objects.filter( state='Austria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_australi = CustomerOrders.objects.filter( state='Australi', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_armenia = CustomerOrders.objects.filter( state='Armenia', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_argentina = CustomerOrders.objects.filter( state='Argentina', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_angola = CustomerOrders.objects.filter( state='Angola', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_algeria = CustomerOrders.objects.filter( state='Algeria', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_albania = CustomerOrders.objects.filter( state='Albania', date_added=yesterday).aggregate(Sum('product_value'))
    y_orders_afghanistan = CustomerOrders.objects.filter( state='Afghanistan', date_added=yesterday).aggregate(Sum('product_value'))

    html_template = get_template('inventory/daily_orders_state_print.html')
    rendered_html = html_template.render(RequestContext(request, {'t_orders_abia': t_orders_abia,

                                                            't_orders_Jakande' :  t_orders_Jakande,
                                                            't_orders_Sangotedo': t_orders_Sangotedo,
                                                            't_orders_Eleko': t_orders_Eleko,
                                                            't_orders_Ajah': t_orders_Ajah,
                                                            't_orders_Ogba': t_orders_Ogba,
                                                            't_orders_Aguda': t_orders_Aguda,
                                                            't_orders_Ketu': t_orders_Ketu,
                                                            't_orders_VI': t_orders_VI,
                                                            't_orders_Ikotun': t_orders_Ikotun,
                                                            't_orders_Oshodi': t_orders_Oshodi,
                                                            't_orders_Ikeja': t_orders_Ikeja,
                                                            't_orders_Lekki': t_orders_Lekki ,
                                                            't_orders_Apapa': t_orders_Apapa,

                                                            't_orders_adamawa': t_orders_adamawa,
                                                            't_orders_anambra': t_orders_anambra,
                                                            't_orders_akwa_ibom': t_orders_akwa_ibom,
                                                            't_orders_bauchi': t_orders_bauchi,
                                                            't_orders_bayelsa': t_orders_bayelsa,
                                                            't_orders_benue': t_orders_benue,
                                                            't_orders_borno': t_orders_borno,
                                                            't_orders_cross_river': t_orders_cross_river,
                                                            't_orders_delta': t_orders_delta,
                                                            't_orders_ebonyi': t_orders_ebonyi,
                                                            't_orders_enugu': t_orders_enugu,
                                                            't_orders_edo': t_orders_edo,
                                                            't_orders_ekiti': t_orders_ekiti,
                                                            't_orders_gombe': t_orders_gombe,
                                                            't_orders_imo': t_orders_imo,
                                                            't_orders_jigawa': t_orders_jigawa,
                                                            't_orders_kaduna': t_orders_kaduna,
                                                            't_orders_kano': t_orders_kano,
                                                            't_orders_katsina': t_orders_katsina,
                                                            't_orders_kebbi': t_orders_kebbi,
                                                            't_orders_kogi': t_orders_kogi,
                                                            't_orders_kwara': t_orders_kwara,
                                                            't_orders_lagos': t_orders_lagos,
                                                            't_orders_nasarawa': t_orders_nasarawa,
                                                            't_orders_niger': t_orders_niger,
                                                            't_orders_ogun': t_orders_ogun,
                                                            't_orders_ondo': t_orders_ondo,
                                                            't_orders_osun': t_orders_osun,
                                                            't_orders_oyo': t_orders_oyo,
                                                            't_orders_plateau': t_orders_plateau,
                                                            't_orders_rivers': t_orders_rivers,
                                                            't_orders_sokoto': t_orders_sokoto,
                                                            't_orders_taraba': t_orders_taraba,
                                                            't_orders_yobe': t_orders_yobe,
                                                            't_orders_zamfara': t_orders_zamfara,
                                                            't_orders_abuja': t_orders_abuja,
                                                            't_orders_spain': t_orders_spain,
                                                            't_orders_usa': t_orders_usa,
                                                            't_orders_uk': t_orders_uk,
                                                            't_orders_ghana': t_orders_ghana,
                                                            't_orders_canada': t_orders_canada,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_saudi': t_orders_saudi,
                                                            't_orders_south': t_orders_south,
                                                            't_orders_switzerland': t_orders_switzerland,
                                                            't_orders_turkey': t_orders_turkey,
                                                            't_orders_zimbabwe' : t_orders_zimbabwe,
                                                            't_orders_zambia':  t_orders_zambia,
                                                            't_orders_yemen': t_orders_yemen,
                                                            't_orders_venezuela': t_orders_venezuela,
                                                            't_orders_uzbekistan': t_orders_uzbekistan,
                                                            't_orders_uruguay': t_orders_uruguay,
                                                            't_orders_uae': t_orders_uae,
                                                            't_orders_ukraine': t_orders_ukraine,
                                                            't_orders_uganda': t_orders_uganda,
                                                            't_orders_tunisia': t_orders_tunisia,
                                                            't_orders_trinidad': t_orders_trinidad,
                                                            't_orders_togo': t_orders_togo,
                                                            't_orders_thailand': t_orders_thailand,
                                                            't_orders_tanzania': t_orders_tanzania,
                                                            't_orders_taiwan': t_orders_taiwan,
                                                            't_orders_sweden': t_orders_sweden,
                                                            't_orders_swaziland': t_orders_swaziland,
                                                            't_orders_sudan': t_orders_sudan,
                                                            't_orders_sri': t_orders_sri,
                                                            't_orders_somalia': t_orders_somalia,
                                                            't_orders_solomon': t_orders_solomon,
                                                            't_orders_slovenia': t_orders_slovenia,
                                                            't_orders_slovakia': t_orders_slovakia,
                                                            't_orders_singapore': t_orders_singapore,
                                                            't_orders_sierra': t_orders_sierra,
                                                            't_orders_serbia': t_orders_serbia,
                                                            't_orders_senegal': t_orders_senegal,
                                                            't_orders_san': t_orders_san,
                                                            't_orders_rwanda': t_orders_rwanda,
                                                            't_orders_russia': t_orders_russia,
                                                            't_orders_romania': t_orders_romania,
                                                            't_orders_qatar': t_orders_qatar,
                                                            't_orders_portugal': t_orders_portugal,
                                                            't_orders_poland': t_orders_poland,
                                                            't_orders_philippines': t_orders_philippines,
                                                            't_orders_peru': t_orders_peru,
                                                            't_orders_paraguay': t_orders_paraguay,
                                                            't_orders_pakistan': t_orders_pakistan,
                                                            't_orders_oman': t_orders_oman,
                                                            't_orders_norway': t_orders_norway,
                                                            't_orders_niue': t_orders_niue,
                                                            't_orders_niger':  t_orders_niger,
                                                            't_orders_nicaragua': t_orders_nicaragua,
                                                            't_orders_newz': t_orders_newz,
                                                            't_orders_netherlands': t_orders_netherlands,
                                                            't_orders_nepal': t_orders_nepal,
                                                            't_orders_namibia': t_orders_namibia,
                                                            't_orders_mozambique': t_orders_mozambique,
                                                            't_orders_morocco': t_orders_morocco,
                                                            't_orders_montenegro': t_orders_montenegro,
                                                            't_orders_mongolia': t_orders_mongolia,
                                                            't_orders_moldova': t_orders_moldova,
                                                            't_orders_mexico': t_orders_mexico,
                                                            't_orders_mauritius': t_orders_mauritius,
                                                            't_orders_mauritania': t_orders_mauritania,
                                                            't_orders_malta': t_orders_malta,
                                                            't_orders_mali': t_orders_mali,
                                                            't_orders_malaysia': t_orders_malaysia,
                                                            't_orders_malawi': t_orders_malawi,
                                                            't_orders_madagascar': t_orders_madagascar,
                                                            't_orders_luxembourg': t_orders_luxembourg,
                                                            't_orders_lithuania': t_orders_lithuania,
                                                            't_orders_liechtenstein': t_orders_liechtenstein,
                                                            't_orders_libya': t_orders_libya,
                                                            't_orders_liberia': t_orders_liberia,
                                                            't_orders_lesotho': t_orders_lesotho,
                                                            't_orders_lebanon': t_orders_lebanon,
                                                            't_orders_latvia': t_orders_latvia,
                                                            't_orders_kuwait': t_orders_kuwait,
                                                            't_orders_korea': t_orders_korea,
                                                            't_orders_kenya': t_orders_kenya,
                                                            't_orders_kazakhstan': t_orders_kazakhstan,
                                                            't_orders_jordan': t_orders_jordan,
                                                            't_orders_japan': t_orders_japan,
                                                            't_orders_jamaica': t_orders_jamaica,
                                                            't_orders_italy': t_orders_italy,
                                                            't_orders_israel': t_orders_israel,
                                                            't_orders_ireland': t_orders_ireland,
                                                            't_orders_iran': t_orders_iran,
                                                            't_orders_iraq': t_orders_iraq,
                                                            't_orders_indonesia': t_orders_indonesia,
                                                            't_orders_india': t_orders_india,
                                                            't_orders_iceland': t_orders_iceland,
                                                            't_orders_hungary': t_orders_hungary,
                                                            't_orders_hong': t_orders_hong,
                                                            't_orders_honduras': t_orders_honduras,
                                                            't_orders_haiti': t_orders_haiti,
                                                            't_orders_guineab': t_orders_guineab,
                                                            't_orders_guinea': t_orders_guinea,
                                                            't_orders_guatemala': t_orders_guatemala,
                                                            't_orders_greenland': t_orders_greenland,
                                                            't_orders_greece': t_orders_greece,
                                                            't_orders_gibraltar': t_orders_gibraltar,
                                                            't_orders_germany': t_orders_germany,
                                                            't_orders_georgia': t_orders_georgia,
                                                            't_orders_gambia': t_orders_gambia,
                                                            't_orders_gabon': t_orders_gabon,
                                                            't_orders_france': t_orders_france,
                                                            't_orders_finland': t_orders_finland,
                                                            't_orders_faroe': t_orders_faroe,
                                                            't_orders_ethiopia': t_orders_ethiopia,
                                                            't_orders_estonia': t_orders_estonia,
                                                            't_orders_eritrea': t_orders_eritrea,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_els': t_orders_els,
                                                            't_orders_egypt': t_orders_egypt,
                                                            't_orders_ecuador': t_orders_ecuador,
                                                            't_orders_denmark': t_orders_denmark,
                                                            't_orders_czech': t_orders_czech,
                                                            't_orders_cyprus': t_orders_cyprus,
                                                            't_orders_cuba': t_orders_cuba,
                                                            't_orders_croatia': t_orders_croatia,
                                                            't_orders_ivory': t_orders_ivory,
                                                            't_orders_costa': t_orders_costa,
                                                            't_orders_congo': t_orders_congo,
                                                            't_orders_colombia': t_orders_colombia,
                                                            't_orders_christmas': t_orders_christmas,
                                                            't_orders_china': t_orders_china,
                                                            't_orders_chile': t_orders_chile,
                                                            't_orders_equatorial': t_orders_equatorial,
                                                            't_orders_chad': t_orders_chad,
                                                            't_orders_central': t_orders_central,
                                                            't_orders_cape': t_orders_cape,
                                                            't_orders_cameroo': t_orders_cameroo,
                                                            't_orders_burundi': t_orders_burundi,
                                                            't_orders_burkina': t_orders_burkina,
                                                            't_orders_bulgaria': t_orders_bulgaria,
                                                            't_orders_brazil': t_orders_brazil,
                                                            't_orders_botswana': t_orders_botswana,
                                                            't_orders_bosnia': t_orders_bosnia,
                                                            't_orders_bolivia': t_orders_bolivia,
                                                            't_orders_benin': t_orders_benin,
                                                            't_orders_belgium': t_orders_belgium,
                                                            't_orders_belarus': t_orders_belarus,
                                                            't_orders_barbados': t_orders_barbados,
                                                            't_orders_bangladesh': t_orders_bangladesh,
                                                            't_orders_bahrain': t_orders_bahrain,
                                                            't_orders_bahamas': t_orders_bahamas,
                                                            't_orders_azerbaija': t_orders_azerbaija,
                                                            't_orders_austria': t_orders_austria,
                                                            't_orders_australi': t_orders_australi,
                                                            't_orders_armenia': t_orders_armenia,
                                                            't_orders_argentina': t_orders_argentina,
                                                            't_orders_angola': t_orders_angola,
                                                            't_orders_algeria': t_orders_algeria,
                                                            't_orders_albania': t_orders_albania,
                                                            't_orders_afghanistan': t_orders_afghanistan,

                                                            'y_orders_Jakande' :  y_orders_Jakande,
                                                            'y_orders_Sangotedo': y_orders_Sangotedo,
                                                            'y_orders_Eleko': y_orders_Eleko,
                                                            'y_orders_Ajah': y_orders_Ajah,
                                                            'y_orders_Ogba': y_orders_Ogba,
                                                            'y_orders_Aguda': y_orders_Aguda,
                                                            'y_orders_Ketu': y_orders_Ketu,
                                                            'y_orders_VI': y_orders_VI,
                                                            'y_orders_Ikotun': y_orders_Ikotun,
                                                            'y_orders_Oshodi': y_orders_Oshodi,
                                                            'y_orders_Ikeja': y_orders_Ikeja,
                                                            'y_orders_Lekki': y_orders_Lekki ,
                                                            'y_orders_Apapa': y_orders_Apapa,

                                                            'y_orders_zimbabwe' : y_orders_zimbabwe,
                                                            'y_orders_zambia':  y_orders_zambia,
                                                            'y_orders_yemen': y_orders_yemen,
                                                            'y_orders_venezuela': y_orders_venezuela,
                                                            'y_orders_uzbekistan': y_orders_uzbekistan,
                                                            'y_orders_uruguay': y_orders_uruguay,
                                                            'y_orders_uae': y_orders_uae,
                                                            'y_orders_ukraine': y_orders_ukraine,
                                                            'y_orders_uganda': y_orders_uganda,
                                                            'y_orders_tunisia': y_orders_tunisia,
                                                            'y_orders_trinidad': y_orders_trinidad,
                                                            'y_orders_togo': y_orders_togo,
                                                            'y_orders_thailand': y_orders_thailand,
                                                            'y_orders_tanzania': y_orders_tanzania,
                                                            'y_orders_taiwan': y_orders_taiwan,
                                                            'y_orders_sweden': y_orders_sweden,
                                                            'y_orders_swaziland': y_orders_swaziland,
                                                            'y_orders_sudan': y_orders_sudan,
                                                            'y_orders_sri': y_orders_sri,
                                                            'y_orders_somalia': y_orders_somalia ,
                                                            'y_orders_solomon': y_orders_solomon,
                                                            'y_orders_slovenia': y_orders_slovenia,
                                                            'y_orders_slovakia': y_orders_slovakia,
                                                            'y_orders_singapore': y_orders_singapore,
                                                            'y_orders_sierra': y_orders_sierra,
                                                            'y_orders_serbia': y_orders_serbia,
                                                            'y_orders_senegal': y_orders_senegal,
                                                            'y_orders_san': y_orders_san,
                                                            'y_orders_rwanda': y_orders_rwanda,
                                                            'y_orders_russia': y_orders_russia,
                                                            'y_orders_romania': y_orders_romania,
                                                            'y_orders_qatar': y_orders_qatar,
                                                            'y_orders_portugal': y_orders_portugal,
                                                            'y_orders_poland': y_orders_poland,
                                                            'y_orders_philippines': y_orders_philippines,
                                                            'y_orders_peru': y_orders_peru,
                                                            'y_orders_paraguay': y_orders_paraguay,
                                                            'y_orders_pakistan': y_orders_pakistan,
                                                            'y_orders_oman': y_orders_oman,
                                                            'y_orders_norway': y_orders_norway,
                                                            'y_orders_niue': y_orders_niue,
                                                            'y_orders_niger':  y_orders_niger,
                                                            'y_orders_nicaragua': y_orders_nicaragua,
                                                            'y_orders_newz': y_orders_newz,
                                                            'y_orders_netherlands': y_orders_netherlands,
                                                            'y_orders_nepal': y_orders_nepal,
                                                            'y_orders_namibia': y_orders_namibia,
                                                            'y_orders_mozambique': y_orders_mozambique,
                                                            'y_orders_morocco': y_orders_morocco,
                                                            'y_orders_montenegro': y_orders_montenegro,
                                                            'y_orders_mongolia': y_orders_mongolia,
                                                            'y_orders_moldova': y_orders_moldova,
                                                            'y_orders_mexico': y_orders_mexico,
                                                            'y_orders_mauritius': y_orders_mauritius,
                                                            'y_orders_mauritania': y_orders_mauritania,
                                                            'y_orders_malta': y_orders_malta,
                                                            'y_orders_mali': y_orders_mali,
                                                            'y_orders_malaysia': y_orders_malaysia,
                                                            'y_orders_malawi': y_orders_malawi,
                                                            'y_orders_madagascar': y_orders_madagascar,
                                                            'y_orders_luxembourg': y_orders_luxembourg,
                                                            'y_orders_lithuania': y_orders_lithuania,
                                                            'y_orders_liechtenstein': y_orders_liechtenstein,
                                                            'y_orders_libya': y_orders_libya,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_lesotho': y_orders_lesotho,
                                                            'y_orders_lebanon': y_orders_lebanon,
                                                            'y_orders_latvia': y_orders_latvia,
                                                            'y_orders_kuwait': y_orders_kuwait,
                                                            'y_orders_korea': y_orders_korea,
                                                            'y_orders_kenya': y_orders_kenya,
                                                            'y_orders_kazakhstan': y_orders_kazakhstan,
                                                            'y_orders_jordan': y_orders_jordan,
                                                            'y_orders_japan': y_orders_japan,
                                                            'y_orders_jamaica': y_orders_jamaica,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_israel': y_orders_israel,
                                                            'y_orders_ireland': y_orders_ireland,
                                                            'y_orders_iran': y_orders_iran,
                                                            'y_orders_iraq': y_orders_iraq,
                                                            'y_orders_indonesia': y_orders_indonesia,
                                                            'y_orders_india': y_orders_india,
                                                            'y_orders_iceland': y_orders_iceland,
                                                            'y_orders_hungary': y_orders_hungary,
                                                            'y_orders_hong': y_orders_hong,
                                                            'y_orders_honduras': y_orders_honduras,
                                                            'y_orders_haiti': y_orders_haiti,
                                                            'y_orders_guineab': y_orders_guineab,
                                                            'y_orders_guinea': y_orders_guinea,
                                                            'y_orders_guatemala': y_orders_guatemala,
                                                            'y_orders_greenland': y_orders_greenland,
                                                            'y_orders_greece': y_orders_greece,
                                                            'y_orders_gibraltar': y_orders_gibraltar,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_georgia': y_orders_georgia,
                                                            'y_orders_gambia': y_orders_gambia,
                                                            'y_orders_gabon': y_orders_gabon,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_finland': y_orders_finland,
                                                            'y_orders_faroe': y_orders_faroe,
                                                            'y_orders_ethiopia': y_orders_ethiopia,
                                                            'y_orders_estonia': y_orders_estonia,
                                                            'y_orders_eritrea': y_orders_eritrea,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_els': y_orders_els,
                                                            'y_orders_egypt': y_orders_egypt,
                                                            'y_orders_ecuador': y_orders_ecuador,
                                                            'y_orders_denmark': y_orders_denmark,
                                                            'y_orders_czech': y_orders_czech,
                                                            'y_orders_cyprus': y_orders_cyprus,
                                                            'y_orders_cuba': y_orders_cuba,
                                                            'y_orders_croatia': y_orders_croatia,
                                                            'y_orders_ivory': y_orders_ivory,
                                                            'y_orders_costa': y_orders_costa,
                                                            'y_orders_congo': y_orders_congo,
                                                            'y_orders_colombia': y_orders_colombia,
                                                            'y_orders_christmas': y_orders_christmas,
                                                            'y_orders_china': y_orders_china,
                                                            'y_orders_chile': y_orders_chile,
                                                            'y_orders_equatorial': y_orders_equatorial,
                                                            'y_orders_chad': y_orders_chad,
                                                            'y_orders_central': y_orders_central,
                                                            'y_orders_cape': y_orders_cape,
                                                            'y_orders_cameroo': y_orders_cameroo,
                                                            'y_orders_burundi': y_orders_burundi,
                                                            'y_orders_burkina': y_orders_burkina,
                                                            'y_orders_bulgaria': y_orders_bulgaria,
                                                            'y_orders_brazil': y_orders_brazil,
                                                            'y_orders_botswana': y_orders_botswana,
                                                            'y_orders_bosnia': y_orders_bosnia,
                                                            'y_orders_bolivia': y_orders_bolivia,
                                                            'y_orders_benin': y_orders_benin,
                                                            'y_orders_belgium': y_orders_belgium,
                                                            'y_orders_belarus': y_orders_belarus,
                                                            'y_orders_barbados': y_orders_barbados,
                                                            'y_orders_bangladesh': y_orders_bangladesh,
                                                            'y_orders_bahrain': y_orders_bahrain,
                                                            'y_orders_bahamas': y_orders_bahamas,
                                                            'y_orders_azerbaija': y_orders_azerbaija,
                                                            'y_orders_austria': y_orders_austria,
                                                            'y_orders_australi': y_orders_australi,
                                                            'y_orders_armenia': y_orders_armenia,
                                                            'y_orders_argentina': y_orders_argentina,
                                                            'y_orders_angola': y_orders_angola,
                                                            'y_orders_algeria': y_orders_algeria,
                                                            'y_orders_albania': y_orders_albania,
                                                            'y_orders_afghanistan': y_orders_afghanistan,
                                                            'product_value_total': product_value_total,
                                                            'y_orders_abia': y_orders_abia,
                                                            'y_orders_adamawa': y_orders_adamawa,
                                                            'y_orders_anambra': y_orders_anambra,
                                                            'y_orders_akwa_ibom': y_orders_akwa_ibom,
                                                            'y_orders_bauchi': y_orders_bauchi,
                                                            'y_orders_bayelsa': y_orders_bayelsa,
                                                            'y_orders_benue': y_orders_benue,
                                                            'y_orders_borno': y_orders_borno,
                                                            'y_orders_cross_river': y_orders_cross_river,
                                                            'y_orders_delta': y_orders_delta,
                                                            'y_orders_ebonyi': y_orders_ebonyi,
                                                            'y_orders_enugu': y_orders_enugu,
                                                            'y_orders_edo': y_orders_edo,
                                                            'y_orders_ekiti': y_orders_ekiti,
                                                            'y_orders_gombe': y_orders_gombe,
                                                            'y_orders_imo': y_orders_imo,
                                                            'y_orders_jigawa': y_orders_jigawa,
                                                            'y_orders_kaduna': y_orders_kaduna,
                                                            'y_orders_kano': y_orders_kano,
                                                            'y_orders_katsina': y_orders_katsina,
                                                            'y_orders_kebbi': y_orders_kebbi,
                                                            'y_orders_kogi': y_orders_kogi,
                                                            'y_orders_kwara': y_orders_kwara,
                                                            'y_orders_lagos': y_orders_lagos,
                                                            'y_orders_nasarawa': y_orders_nasarawa,
                                                            'y_orders_niger': y_orders_niger,
                                                            'y_orders_ogun': y_orders_ogun,
                                                            'y_orders_ondo': y_orders_ondo,
                                                            'y_orders_osun': y_orders_osun,
                                                            'y_orders_oyo': y_orders_oyo,
                                                            'y_orders_plateau': y_orders_plateau,
                                                            'y_orders_rivers': y_orders_rivers,
                                                            'y_orders_sokoto': y_orders_sokoto,
                                                            'y_orders_taraba': y_orders_taraba,
                                                            'y_orders_yobe': y_orders_yobe,
                                                            'y_orders_zamfara': y_orders_zamfara,
                                                            'y_orders_abuja': y_orders_abuja,
                                                            'y_orders_spain': y_orders_spain,
                                                            'y_orders_usa': y_orders_usa,
                                                            'y_orders_uk': y_orders_uk,
                                                            'y_orders_ghana': y_orders_ghana,
                                                            'y_orders_canada': y_orders_canada,
                                                            'y_orders_france': y_orders_france,
                                                            'y_orders_germany': y_orders_germany,
                                                            'y_orders_italy': y_orders_italy,
                                                            'y_orders_liberia': y_orders_liberia,
                                                            'y_orders_saudi': y_orders_saudi,
                                                            'y_orders_south': y_orders_south,
                                                            'y_orders_switzerland': y_orders_switzerland,
                                                            'y_orders_turkey': y_orders_turkey,
                                                            'product_value_total_y': product_value_total_y})).encode(encoding="UTF-8")

    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css')])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename=' + str(today) +"Daily Orders By State.pdf"

    return http_response



@login_required
def delivery_person_charges(request):
    #cat = DeliveryPersonCharges.objects.get(id=id)
    my_form = DeliveryPersonChargesForm()
    if request.method == 'POST':
        capital_new = int(request.POST['capital'])
        commission_new = int(request.POST['commission'])
        incentive_new = int(request.POST['incentive'])
        expenses_new = int(request.POST['expenses'])
        next_capital_new = int(request.POST['next_capital'])
        capital_left = capital_new - expenses_new
        form = DeliveryPersonChargesForm(request.POST)
        if form.is_valid():
            delivery_person = form.save(commit=False)
            delivery_person.total = abs(capital_left) + commission_new + incentive_new + next_capital_new
            delivery_person.save()
            form = my_form
            messages.success(request, ' Delivery Person Charges Added Successfully, You can Add Another')
            return render(request, 'inventory/add_delivery_person_charges.html', {'form': form})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Form')
    else:
        form = my_form
    return render(request, 'inventory/add_delivery_person_charges.html', {
        'form': form
    })


@login_required
def delivery_person_cash(request):
    is_dperson = request.user.groups.filter(name='dperson').exists()
    #cat = DeliveryPersonCharges.objects.get(id=id)
    my_form = DeliveryPersonCashForm()
    if request.method == 'POST':
        count_new = int(request.POST['count'])
        form = DeliveryPersonCashForm(request.POST)
        if form.is_valid():
            delivery_person = form.save(commit=False)
            delivery_person.total = count_new * 400
            delivery_person.save()
            form = my_form
            messages.success(request, ' Delivery Person Cash details Added Successfully, You can Add Another')
            return render(request, 'inventory/add_delivery_person_cash.html', {'form': form, 'is_dperson': is_dperson})
        else:
            messages.error(request, 'Oops!!! There are Some Errors in your Form')
    else:
        form = my_form
    return render(request, 'inventory/add_delivery_person_cash.html', {
        'form': form, 'is_dperson': is_dperson,
    })


@login_required
def all_delivery_person_cash(request):

    is_dperson = request.user.groups.filter(name='dperson').exists()
    all_delivery_person_cash = DeliveryPersonCash.objects.all().order_by('-id')
    emeka_cash = DeliveryPersonCash.objects.filter(d_person="emeka", date_added__gte=last_week).aggregate(Sum('total'))
    alex_cash = DeliveryPersonCash.objects.filter(d_person="alex", date_added__gte=last_week).aggregate(Sum('total'))
    yinka_cash = DeliveryPersonCash.objects.filter(d_person="yinka", date_added__gte=last_week).aggregate(Sum('total'))
    collins_cash = DeliveryPersonCash.objects.filter(d_person="collins", date_added__gte=last_week).aggregate(Sum('total'))
    segun_cash = DeliveryPersonCash.objects.filter(d_person="segun", date_added__gte=last_week).aggregate(Sum('total'))
    richard_cash = DeliveryPersonCash.objects.filter(d_person="richard", date_added__gte=last_week).aggregate(Sum('total'))
    samson_cash = DeliveryPersonCash.objects.filter(d_person="samson", date_added__gte=last_week).aggregate(Sum('total'))
    emmanuel_cash = DeliveryPersonCash.objects.filter(d_person="emmanuel", date_added__gte=last_week).aggregate(Sum('total'))
    justine_cash = DeliveryPersonCash.objects.filter(d_person="justine", date_added__gte=last_week).aggregate(Sum('total'))


    paginator = Paginator(all_delivery_person_cash, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/all_delivery_person_cash.html', {'orders': all_delivery_person_cash,
                                                                'is_dperson': is_dperson,
                                                                'emeka_cash':  emeka_cash,
                                                                'alex_cash':  alex_cash,
                                                                'yinka_cash':  yinka_cash,
                                                                'collins_cash':  collins_cash,
                                                                'segun_cash':  segun_cash,
                                                                'richard_cash':  richard_cash,
                                                                'samson_cash':  samson_cash,
                                                                'emmanuel_cash':  emmanuel_cash,
                                                                'justine_cash':  justine_cash,

                                                               'orderss': orderss})


@login_required
def all_delivery_person_charges(request):
    all_delivery_person_charges = DeliveryPersonCharges.objects.all().order_by('-id')
    sum_all_charges = DeliveryPersonCharges.objects.all().aggregate(Sum('total'))
    paginator = Paginator(all_delivery_person_charges, 10)
    page = request.GET.get('page')
    try:
        orderss = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orderss = paginator.page(paginator.num_pages)
    return render(request, 'inventory/all_delivery_person_charges.html', {'orders': all_delivery_person_charges, 'sum_all_charges': sum_all_charges,
                                                               'orderss': orderss})


@login_required
def delete_d_person(request, id):
    DeliveryPersonCharges.objects.get(id=id).delete()
    next = request.GET.get('next')
    messages.success(request, ' Delivery Person Charges Deleted Successfully')
    return redirect(next)