from django.db import models


class DebtStatus(models.TextChoices):
    INACTIVE = "INACTIVE", "Inactive"
    PAID_IN_FULL = "PAID_IN_FULL", "Paid in full"
    IN_COLLECTION = "IN_COLLECTION", "In collection"
