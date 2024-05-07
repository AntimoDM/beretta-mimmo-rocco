from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Cliente, Intervento, TecnicoCaldaia, NumeroDiTelefonoAggiuntivo
from .serializers import CustomerSerializer, ClienteSerializer, InterventoSerializer, TecnicoCaldaiaSerializer, NumeroDiTelefonoAggiuntivoSerializer


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


class ClienteListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = Cliente.objects.all()
        serializer = ClienteSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteDettaglioApiView(APIView):

    def _get_object(self, numero_di_telefono):
        try:
            return Cliente.objects.get(telefono_principale=numero_di_telefono)
        except Cliente.DoesNotExist:
            return None

    def _get_response(self, object_instance):
        serializer = ClienteSerializer(object_instance)
        data = serializer.data
        interventi_serializer = InterventoSerializer(object_instance.intervento_set.all(), many=True)
        data.update({"interventi": interventi_serializer.data})
        numeri_aggiuntivi_serializer = NumeroDiTelefonoAggiuntivoSerializer(object_instance.numeroditelefonoaggiuntivo_set.all(), many=True)
        data.update({"numeri_aggiuntivi": numeri_aggiuntivi_serializer.data})
        return data

    def get(self, request, numero_di_telefono, *args, **kwargs):
        cliente = self._get_object(numero_di_telefono)
        if not cliente:
            # devo cercare tra i numeri aggiuntivi

            return Response(
                {"res": "Cliente non trovato"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = self._get_response(cliente)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, numero_di_telefono):
        cliente = self._get_object(numero_di_telefono)

        if not cliente:
            return Response(
                {"res": "Cliente non trovato"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response("Parametri Errati", status.HTTP_400_BAD_REQUEST)

        data = self._get_response(cliente)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, numero_di_telefono, format=None):
        try:
            cliente = Cliente.objects.get(id=numero_di_telefono)
            cliente.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Cliente.DoesNotExist:
            return Response(
                {"res": "Cliente non trovato"},
                status=status.HTTP_400_BAD_REQUEST
            )


class InterventoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        """
        List all the Customer items
        """
        objects = Intervento.objects.all()
        serializer = InterventoSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Customer with given Customer data
        """
        data = {
            'data_chiamata': request.data.get('data_chiamata'),
            'data_completamento': request.data.get('data_completamento'),
            'data_assegnamento': request.data.get('data_assegnamento'),
            'motivazione': request.data.get('motivazione'),
            'note_per_tecnico': request.data.get('note_per_tecnico'),
            'note_del_tecnico': request.data.get('note_del_tecnico'),
            'stato': request.data.get('stato'),
            'cliente': request.data.get('cliente'),
        }
        serializer = InterventoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterventoDettaglioApiView(APIView):

    def get_object(self, _id):
        """
        Helper method to get the object with given customer_id
        """
        try:
            return Intervento.objects.get(id=_id)
        except Intervento.DoesNotExist:
            return None

    def get(self, request, _id, *args, **kwargs):
        """
        Retrieves the food with given customer_id
        """
        customer_instance = self.get_object(_id)
        if not customer_instance:
            return Response(
                {"res": "Intervento non trovato"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InterventoSerializer(customer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, _id):
        obj = self.get_object(_id)
        if not obj:
            return Response(
                {"res": "Intervento non trovato"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InterventoSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("wrong parameters", status.HTTP_400_BAD_REQUEST)

    def delete(self, request, _id, format=None):
        obj = self.get_object(_id)
        if not obj:
            return Response(
                {"res": "Intervento non trovato"},
                status=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TecnicoCaldaiaListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = TecnicoCaldaia.objects.all()
        serializer = TecnicoCaldaiaSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TecnicoCaldaiaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumeroDiTelefonoAggiuntivoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = NumeroDiTelefonoAggiuntivo.objects.all()
        serializer = NumeroDiTelefonoAggiuntivoSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = NumeroDiTelefonoAggiuntivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)