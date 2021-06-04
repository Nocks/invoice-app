import datetime
import random
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from . forms import InvoiceForm, VendorForm, ClientForm, ProjectItemForm
from . models import Client, Invoice, ProjectItem


ALPHABETS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
NUMBERS = [1, 2, 3, 5, 6, 7, 8, 9, 0]


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


def get_payment_due_date(selected_invoice_date, selected_payment_terms):
    payment_duration = None
    if selected_payment_terms == 'net_1':
        payment_duration = 1
    elif selected_payment_terms == 'net_7':
        payment_duration = 7
    elif selected_payment_terms == 'net_14':
        payment_duration = 14
    else:
        payment_duration = 30
    invoice_date = datetime.date.fromisoformat(str(selected_invoice_date))
    payment_due_date = invoice_date + datetime.timedelta(days=payment_duration)
    return payment_due_date


def create_invoice(request):
    if request.POST:
        print(request.POST)
        vendor_form = VendorForm(request.POST)
        client_form = ClientForm(request.POST)
        invoice_form = InvoiceForm(request.POST)
        project_item_form = ProjectItemForm(request.POST)
        
        if (
            vendor_form.is_valid() and 
            client_form.is_valid() and 
            invoice_form.is_valid() and 
            project_item_form.is_valid()
        ):
            generated_invoice_code = generate_invoice_code()
            # Create an invoice instance and set its code with the 
            # generated_invoice_code
            new_invoice = Invoice.objects.create(code=generated_invoice_code)

            # Create client instance and set its fields with details from the form
            invoice_client = Client.objects.create(
                invoice_code=Invoice.objects.get(code=generated_invoice_code),
                name=client_form.cleaned_data["name"],
                email=client_form.cleaned_data["email"],
                street_address=client_form.cleaned_data["street_address"],
                city=client_form.cleaned_data["city"],
                post_code=client_form.cleaned_data["post_code"],
                country=client_form.cleaned_data["country"]
            )

            # Create project items
            for i in range(len(request.POST.getlist("item_name"))):
                ProjectItem.objects.create(
                    invoice_code=Invoice.objects.get(code=generated_invoice_code),
                    item_name=request.POST.getlist("item_name")[i],
                    item_quantity=request.POST.getlist("item_quantity")[i],
                    item_price=request.POST.getlist("item_price")[i],
                    item_total=request.POST.getlist("item_total")[i],
                )

            # Set the client of the invoice
            new_invoice.client = invoice_client
            new_invoice.project_description = invoice_form.cleaned_data[
                "project_description"
            ]
            # Set invoice status based on the button clicked
            if request.POST["invoice-process"] == 'save-draft':
                new_invoice.status = 'draft'
            else:
                new_invoice.status = 'pending'
            # Set selected payment terms
            if invoice_form.cleaned_data["payment_terms"] == "net_1":
                new_invoice.payment_terms = "net_1"
            elif invoice_form.cleaned_data["payment_terms"] == "net_7":
                new_invoice.payment_terms = "net_7"
            elif invoice_form.cleaned_data["payment_terms"] == "net_14":
                new_invoice.payment_terms = "net_14"
            else:
                new_invoice.payment_terms = "net_30"
            # Set selected date
            new_invoice.date = invoice_form.cleaned_data["date"]
            # Calculate and set payment due date
            new_invoice.due_date = get_payment_due_date(
                invoice_form.cleaned_data["date"], request.POST["payment_terms"]
            )
            new_invoice.total = ProjectItem.objects.filter(
                invoice_code__code=generated_invoice_code
            ).aggregate(Sum('item_total')).get('item_total__sum')
            # Save the newly created invoice
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