from django import forms
from . models import Vendor, Client, Invoice, ProjectItem


class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        fields = [
            "project_description",
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
            "v_name",
            "v_street_address",
            "v_city",
            "v_post_code",
            "v_country",
        ]
        labels = {
            "v_name": "Name",
            "v_street_address": "Street Address",
            "v_city": "City",
            "v_post_code": "Post Code",
            "v_country": "Country"
        }


class ProjectItemForm(forms.ModelForm):

    class Meta:
        model = ProjectItem
        fields = [
            "item_name",
            "item_quantity",
            "item_price",
            "item_total"
        ]
        labels = {
            "item_name": "Name",
            "item_quantity": "Quantity",
            "item_price": "Price",
            "item_total": "Total"
        }