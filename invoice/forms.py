from django import forms
from . models import Invoice, Vendor, Client


class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        fields = [
            "project_description",
            "status",
            "date",
            "payment_terms",
        ]


class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "street_address",
            "city",
            "post_code",
            "country",
        ]


class VendorForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = [
            "street_address",
            "city",
            "post_code",
            "country",
        ]