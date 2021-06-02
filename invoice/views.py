import random
from django.shortcuts import render
from django.http import HttpResponse
from . forms import InvoiceForm, VendorForm, ClientForm, ProjectItemForm
from . models import Invoice, Client


ALPHABETS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
NUMBERS = [1, 2, 3, 5, 6, 7,8,9,0]


def generate_invoice_code():
    generated_code = '#'
    while True:
        for i in range(2):
            generated_code += random.choice(ALPHABETS)
        for i in range(4):
            generated_code += str(random.choice(NUMBERS))
        if not Invoice.objects.filter(code=generated_code).exists():
            break
        else:
            generated_code = '#'
    return generated_code


def create_invoice(request):
    if request.POST:
        print(request.POST)
        vendor_form = VendorForm(request.POST)
        client_form = ClientForm(request.POST)
        invoice_form = InvoiceForm(request.POST)
        
        if (
            vendor_form.is_valid() and 
            client_form.is_valid() and 
            invoice_form.is_valid()
        ):
            generated_invoice_code = generate_invoice_code()
            new_invoice = Invoice.objects.create(code=generated_invoice_code)

            invoice_client = Client.objects.create(
                invoice_code=Invoice.objects.get(code=generated_invoice_code),
                name=client_form.cleaned_data["name"],
                email=client_form.cleaned_data["email"],
                street_address=client_form.cleaned_data["street_address"],
                city=client_form.cleaned_data["city"],
                post_code=client_form.cleaned_data["post_code"],
                country=client_form.cleaned_data["country"]
            )

            new_invoice.client = invoice_client
            new_invoice.project_description = invoice_form.cleaned_data["project_description"]
            if request.POST["invoice-process"] == 'save-draft':
                new_invoice.status = 'draft'
            else:
                new_invoice.status = 'pending'
            new_invoice.save()

    vendor_form = VendorForm()
    client_form = ClientForm()
    invoice_form = InvoiceForm()
    project_item_form = ProjectItemForm()

    return render(request, 'invoice/new_invoice.html',
        {
            'vendor_form': vendor_form,
            'client_form': client_form,
            'invoice_form': invoice_form,
            'project_item_form': project_item_form,
        }
    )