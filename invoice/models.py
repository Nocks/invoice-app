from django.db import models


DRAFT = 'draft'
PENDING = 'pending'
PAID = 'paid'

INVOICE_STATUS = (
    (DRAFT, 'Draft'),
    (PENDING, 'Pending'),
    (PAID, 'Paid'),
)

NET_1 = 'net_1'
NET_7 = 'net_7'
NET_14 = 'net_14'
NET_30 = 'net_30'

PAYMENT_TERMS = [
    (NET_1, 'Net 1 Day'),
    (NET_7, 'Net 7 Days'),
    (NET_14, 'Net 14 Days'),
    (NET_30, 'Net 30 Days'),
]

ALPHABETS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
NUMBERS = [1, 2, 3, 5, 6, 7,8,9,0]


class Invoice(models.Model):
    code = models.CharField(max_length=7, unique=True)
    client = models.ForeignKey(
        'Client', related_name='invoices', on_delete=models.CASCADE, null=True
    )
    project_description = models.CharField(max_length=60, null=True)
    status = models.CharField(
        max_length=7,
        choices=INVOICE_STATUS,
        default=DRAFT
    )
    payment_terms = models.CharField(
        max_length=6,
        choices=PAYMENT_TERMS,
        default=NET_30,
    )
    date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    due_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=500)

    def __str__(self):
        return self.code


class Client(models.Model):
    invoice_code = models.ForeignKey(
        Invoice, related_name='clients', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254)
    street_address = models.CharField(max_length=70)
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProjectItem(models.Model):
    invoice_code = models.ForeignKey(
        Invoice, related_name='project_items', on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length=80)
    item_quantity = models.PositiveSmallIntegerField()
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    item_total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    # It will be great to have user on this model
    v_name = models.CharField(max_length=80)
    v_street_address = models.CharField(max_length=70)
    v_city = models.CharField(max_length=30)
    v_post_code = models.CharField(max_length=10)
    v_country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

