from django.shortcuts import render
from django.http import HttpResponse
from . forms import InvoiceForm, VendorForm, ClientForm


def create_invoice(request):
    vendor_form = VendorForm()
    client_form = ClientForm()
    invoice_form = InvoiceForm()

    return render(request, 'invoice/new_invoice.html',
        {
            'vendor_form': vendor_form,
            'client_form': client_form,
            'invoice_form': invoice_form,
        }
    )