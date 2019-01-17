from django import forms
from inventory.models import CustomerOrders, ComsReps, Category, \
 StateCountry, DeliveryPerson, OrderStatus, Status, Stock, DeliveryPersonCharges, LagosLocations, DeliveryPersonCash


class CustomerOrderForm(forms.ModelForm):

    def __init__(self, category, *args, **kwargs):
        super(CustomerOrderForm, self).__init__(*args, **kwargs)
        self.fields['state'] = forms.ChoiceField([(o.name, str(o)) for o in StateCountry.objects.all()])

    class Meta:
        model = CustomerOrders
        exclude = ('user', 'date_added', 'time', 'date', 'cust_code', 'amount_paid', 'date_paid', 'd_person', 'order_status', 'comment', 'confirmer', 'coms_exec', 'status', 'category')


class LagosCustomerOrderForm(forms.ModelForm):

    def __init__(self, category, *args, **kwargs):
        super(LagosCustomerOrderForm, self).__init__(*args, **kwargs)
        self.fields['coms_exec'] = forms.ChoiceField(
            choices=[(o.user, str(o)) for o in ComsReps.objects.filter(category=category)]
        )
        self.fields['state'] = forms.ChoiceField([(o.name, str(o)) for o in LagosLocations.objects.all()])
        self.fields['status'] = forms.ChoiceField([(o.name, str(o)) for o in Status.objects.all()])

    class Meta:
        model = CustomerOrders
        exclude = ('user', 'date_added', 'time', 'date', 'cust_code', 'amount_paid', 'date_paid', 'd_person', 'category', 'order_status', 'comment', 'confirmer')


class ConfirmCustomerOrderForm(forms.ModelForm):
    def __init__(self, category, *args, **kwargs):
        super(ConfirmCustomerOrderForm, self).__init__(*args, **kwargs)

        self.fields['state'] = forms.ChoiceField([(o.name, str(o)) for o in StateCountry.objects.all()])

    class Meta:
        model = CustomerOrders
        exclude = (
        'user', 'date_added', 'time', 'date', 'cust_code', 'category', 'comment', 'status', 'order_status', 'confirmer', 'd_person', 'coms_exec')


class OrderStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderStatusForm, self).__init__(*args, **kwargs)

        self.fields['order_status'] = forms.ChoiceField([(o.name, str(o)) for o in OrderStatus.objects.all()])

    class Meta:
        model = CustomerOrders
        fields = ('order_status', 'comment' )


class DeliveryPersonChargesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeliveryPersonChargesForm, self).__init__(*args, **kwargs)

        self.fields['d_person'] = forms.ChoiceField([(o.name, str(o)) for o in DeliveryPerson.objects.all()])

    class Meta:
        model = DeliveryPersonCharges
        fields = '__all__'


class DeliveryPersonCashForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeliveryPersonCashForm, self).__init__(*args, **kwargs)

        self.fields['d_person'] = forms.ChoiceField([(o.name, str(o)) for o in DeliveryPerson.objects.all()])

    class Meta:
        model = DeliveryPersonCash
        fields = '__all__'


class StockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.ChoiceField([(o.name, str(o)) for o in StateCountry.objects.all()])

    class Meta:
        model = Stock
        exclude = ('add_stock', 'substract_stock', 'current_stock', 'date_updated',
                    'ginger_me_value', 'cocoa_my_koko_value', 'green_with_envy_value', 'inighe_value',
                    'la_vida_loca_value', 'nutty_by_nature_value', 'triple_threat_value', 'total', 'remarks',)


class AddStockForm(forms.ModelForm):

    class Meta:
        model = Stock
        exclude = ('add_stock', 'substract_stock', 'current_stock')


class RemoveStockForm(forms.ModelForm):

    class Meta:
        model = Stock
        exclude = ('add_stock', 'substract_stock', 'current_stock')
