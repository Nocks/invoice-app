from django.db import models


INVOICE_STATUS = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('paid', 'Paid'),
)


PAYMENT_TERMS = (
    ('net_1', 'Net 1 Day'),
    ('net_7', 'Net 7 Days'),
    ('net_14', 'Net 14 Days'),
    ('net_30', 'Net 30 Days'),
)


class Invoice(models.Model):
    code = models.CharField(max_length=7, unique=True)
    client = models.ForeignKey(
        'Client', related_name='invoices', on_delete=models.CASCADE
    )
    project_description = models.CharField(
        max_length=60, blank=True, null=True
    )
    status = models.CharField(
        max_length=7, choices=INVOICE_STATUS, blank=True, null=True
    )
    payment_status = models.CharField(
        max_length=6, choices=PAYMENT_TERMS, blank=True, null=True
    )
    date = models.DateField(auto_now_add=True, auto_now=False)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    total = models.DecimalField(max_digits=7, decimal_places=2)


    def __str__(self):
        return self.project_description


class Client(models.Model):
    # invoice_code = models.ForeignKey(
    #     Invoice, related_name='clients', on_delete=models.CASCADE
    # )
    name = models.CharField(
        max_length=30, blank=True, null=True, unique=True
    )
    email = models.EmailField(max_length=254)
    street_address = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=50)


    def __str__(self):
        return name


class ProjectItem(models.Model):
    # invoice_code = models.ForeignKey(
    #     Invoice, related_name='clients', on_delete=models.CASCADE
    # )
    name = models.CharField(max_length=80, blank=False, null=False)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)


    def __str__(self):
        return name


class Vendor(models.Model):
    # It will be great to have user on this model
    name = models.CharField(max_length=80, blank=False, null=False)
    street_address = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=50)


    def __str__(self):
        return name

