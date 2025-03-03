from django.db import models
from .choices import DebtStatus


class CollectionAgency(models.Model):
    name = models.CharField(max_length=100)


# Files uploaded by a collection agency
class CollectionFiles(models.Model):
    file = models.FileField(verbose_name="Files", upload_to="CollectionFiles/%Y/%m/%d", null=False, blank=False)
    collection_agency = models.ForeignKey(CollectionAgency, on_delete=models.CASCADE, related_name='agency')


# Clients that hires a collection agency and also has consumers
class Client(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    collection_agency = models.ForeignKey(CollectionAgency, on_delete=models.CASCADE, related_name='hiredAgency')


# Consumers that own the debt
class Consumer(models.Model):
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=100, unique=True)
    ssn = models.CharField(max_length=30, unique=True)


class Debt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='consumer')
    status = models.CharField(
        max_length=30,
        choices=DebtStatus.choices,
        default=DebtStatus.INACTIVE
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'consumer'], name='unique_debt_client_consumer')
        ]
