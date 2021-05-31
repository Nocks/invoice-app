import random
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
    code = models.CharField(max_length=7, blank=True, unique=True)
    client = models.ForeignKey(
        'Client', related_name='invoices', on_delete=models.CASCADE
    )
    project_description = models.CharField(max_length=60)
    status = models.CharField(
        max_length=7,
        choices=INVOICE_STATUS,
        default=DRAFT
    )
    payment_terms = models.CharField(
        max_length=6,
        choices=PAYMENT_TERMS,
        default=NET_30,
        blank=False,
        null=False
    )
    date = models.DateField(auto_now_add=False, auto_now=False)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.project_description
    
    def save(self, *args, **kwargs):
        generated_code = '#'
        for i in range(2):
            generated_code += random.choice(ALPHABETS)
        for i in range(4):
            generated_code += str(random.choice(NUMBERS))
        self.code = generated_code
        super().save(*args, **kwargs)


class Client(models.Model):
    # invoice_code = models.ForeignKey(
    #     Invoice, related_name='clients', on_delete=models.CASCADE
    # )
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254)
    street_address = models.CharField(max_length=70)
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProjectItem(models.Model):
    # invoice_code = models.ForeignKey(
    #     Invoice, related_name='clients', on_delete=models.CASCADE
    # )
    name = models.CharField(max_length=80)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    # It will be great to have user on this model
    name = models.CharField(max_length=80)
    street_address = models.CharField(max_length=70)
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

