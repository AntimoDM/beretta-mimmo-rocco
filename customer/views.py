from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


class CustomerListApiView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all the Customer items
        """
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create the Customer with given Customer data
        """
        data = {
            'name': request.data.get('name'),
            'user': request.user.id
        }
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailApiView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, customer_id):
        """
        Helper method to get the object with given customer_id
        """
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None

    def get(self, request, customer_id, *args, **kwargs):
        """
        Retrieves the food with given customer_id
        """
        customer_instance = self.get_object(customer_id)
        if not customer_instance:
            return Response(
                {"res": "Object with customer id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CustomerSerializer(customer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
