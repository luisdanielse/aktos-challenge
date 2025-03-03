import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import CollectionAgency, Client, Consumer, Debt
from rest_framework import generics
from . serializers import DebtSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .CustomFilters import DebtFilter


"""
Web service to load data into Database
"""
class wsUploadFile(APIView):
    def post(self, request, *args, **kwargs):
        if 'inputFile' not in request.FILES:
            return Response({"error": "File was not provided"}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['inputFile']

        # Verify a CSV file was provided
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be in CSV format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)

            next(reader, None)

            created_rows = 0
            errors = []

            collection_agency, created_agency = CollectionAgency.objects.get_or_create(name="AKTOS AGENCY")

            for index, row in enumerate(reader):
                try:
                    client, created_client = Client.objects.get_or_create(reference=row[0],
                                                                          collection_agency=collection_agency)
                    consumer, created_consumer = Consumer.objects.get_or_create(name=row[3], address=row[4],
                                                                               ssn=row[5])

                    debt, created_debt = Debt.objects.get_or_create(client=client, consumer=consumer,
                                                                    status=row[2], balance=row[1])

                    created_rows += 1
                except ValidationError as e:
                    errors.append(f"Error at row {index + 1}: {str(e)}")

            return Response(
                {"success": f"{created_rows} successfully created", "errors": errors},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": f"Error with processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


"""
Web Service to Get Information about debt
"""


class DebtListView(generics.ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DebtFilter
    ordering_fields = ['balance', 'status']  # Allows ordering by balance or status

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"message": "No debts found with the given criteria."}, status=404)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
