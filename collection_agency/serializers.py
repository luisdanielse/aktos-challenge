from rest_framework import serializers
from .models import Debt

class DebtSerializer(serializers.ModelSerializer):
    consumer_name = serializers.CharField(source='consumer.name', read_only=True)
    client_reference = serializers.CharField(source='client.reference', read_only=True)

    class Meta:
        model = Debt
        fields = ['id', 'client_reference', 'consumer_name', 'status', 'balance']
