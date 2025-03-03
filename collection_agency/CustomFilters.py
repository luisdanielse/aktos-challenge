from .models import Debt
import django_filters


# Custom filtering class
class DebtFilter(django_filters.FilterSet):
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")
    consumer_name = django_filters.CharFilter(field_name="consumer__name", lookup_expr="icontains")
    status = django_filters.CharFilter(method="filter_status")

    class Meta:
        model = Debt
        fields = ['min_balance', 'max_balance', 'consumer_name', 'status']

    def filter_status(self, queryset, name, value):
        return queryset.filter(status=value.upper())  # Convert to uppercase before filtering
