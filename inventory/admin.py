from django.contrib import admin
from django.contrib.admin.models import LogEntry
from inventory.models import CustomerOrders, Category, ComsReps,\
     StateCountry, DeliveryPerson, OrderStatus, Status, Stock, StockValues, LagosLocations, DeliveryPersonCharges, DeliveryPersonCash

# Register your models here.


class CustomerOrdersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomerOrders._meta.fields if field.name != "id"]
    search_fields = ('cust_name', 'phone_no', 'state', 'coms_exec' )
    list_filter = ("category", "state", "order_status", "status")


class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.fields if field.name != "id"]
    search_fields = ('name',)
    list_filter = ("name", "date_updated", )



class ComsRepsAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ("category",)


class LogAdmin(admin.ModelAdmin):
    """Create an admin view of the history/log table"""
    list_display = ('action_time','user','content_type','change_message','is_addition','is_change','is_deletion')
    list_filter = ['action_time','user','content_type']
    ordering = ('-action_time',)
    #We don't want people changing this historical record:
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        #returning false causes table to not show up in admin page :-(
        #I guess we have to allow changing for now
        return True
    def has_delete_permission(self, request, obj=None):
        return False

class StockValuesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StockValues._meta.fields if field.name != "id"]
    search_fields = ('name',)
    list_filter = ("name",)

admin.site.register(CustomerOrders, CustomerOrdersAdmin)
admin.site.register(Category)
admin.site.register(ComsReps, ComsRepsAdmin)
admin.site.register(StateCountry)
admin.site.register(DeliveryPerson)
admin.site.register(OrderStatus)
admin.site.register(Status)
admin.site.register(Stock, StockAdmin)
admin.site.register(LogEntry, LogAdmin)
admin.site.register(StockValues, StockValuesAdmin)
admin.site.register(LagosLocations)
admin.site.register(DeliveryPersonCharges)
admin.site.register(DeliveryPersonCash)