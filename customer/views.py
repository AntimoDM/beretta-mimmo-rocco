import datetime

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Cliente, Intervento, TecnicoCaldaia, NumeroDiTelefonoAggiuntivo, Manutenzione, Garanzia
from .serializers import CustomerSerializer, ClienteSerializer, InterventoSerializer, TecnicoCaldaiaSerializer, \
    NumeroDiTelefonoAggiuntivoSerializer, ManutenzioneSerializer, GaranziaSerializer


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
        numeri_aggiuntivi_serializer = NumeroDiTelefonoAggiuntivoSerializer(
            object_instance.numeroditelefonoaggiuntivo_set.all(), many=True)

        data.update({"numeri_aggiuntivi": numeri_aggiuntivi_serializer.data})
        garanzia = Garanzia.objects.get(cliente=data.get("id"))
        garanzia_serializer = GaranziaSerializer(garanzia, many=False)
        data.update({"garanzia": garanzia_serializer.data})
        manutenzione = Manutenzione.objects.get(cliente=data.get("id"))
        manutenzione_serializer = ManutenzioneSerializer(manutenzione, many=False)
        data.update({"manutenzione": manutenzione_serializer.data})
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
            return Response({"res": "Cliente eliminato con successo"}, status=status.HTTP_200_OK)

        except Cliente.DoesNotExist:
            return Response(
                {"res": "Cliente non trovato"},
                status=status.HTTP_400_BAD_REQUEST
            )


class InterventoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        stato = request.query_params.get("stato")
        tecnico = request.query_params.get("tecnico")

        oggetti = Intervento.objects

        if stato:
            oggetti = oggetti.filter(stato=stato)
        if tecnico:
            oggetti = oggetti.filter(tecnico=tecnico)

        serializer = InterventoSerializer(oggetti, many=True)
        data = serializer.data
        for d in data:
            _id = d.get("cliente")
            cliente = Cliente.objects.get(id=_id)

            d.update({"cliente": {
                "id": d.get("cliente"),
                "nome": cliente.nome,
                "cognome": cliente.cognome,
                "nome_cognome_import": cliente.nome_cognome_import
            }})

            tecnico_id = d.get("tecnico")
            if tecnico_id:
                tecnico = TecnicoCaldaia.objects.get(id=tecnico_id)

                d.update({"tecnico": {
                    "id": d.get("tecnico"),
                    "nome": tecnico.nome,
                }})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Customer with given Customer data
        """
        data = request.data
        if data.get("tecnico"):
            data.update({"data_assegnamento": datetime.datetime.now().date()})
            data.update({"stato": 2})
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
        data = request.data
        if data.get("tecnico"):
            data.update({"data_assegnamento": datetime.datetime.now().date()})
            data.update({"stato": 2})
        if data.get("stato", 0) == 3:
            data.update({"data_completamento": datetime.datetime.now().date()})
        serializer = InterventoSerializer(obj, data=data, partial=True)
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
        return Response({"res": "Intervento eliminato con successo"}, status=status.HTTP_200_OK)


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


class ManutenzioneListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = Manutenzione.objects.all()
        serializer = ManutenzioneSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ManutenzioneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, _id):
        obj = self.get_object(_id)
        if not obj:
            return Response(
                {"res": "Manutenzione non trovata"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        serializer = ManutenzioneSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("wrong parameters", status.HTTP_400_BAD_REQUEST)

    def _get_object(self, _id):
        """
        Helper method to get the object with given customer_id
        """
        try:
            return Manutenzione.objects.get(id=_id)
        except Manutenzione.DoesNotExist:
            return None


class GaranziaListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = Garanzia.objects.all()
        res = []
        for customer in customers:
            res.append(self._get_response(customer))
        return Response(res, status=status.HTTP_200_OK)

    def _get_response(self, object_instance):
        serializer = GaranziaSerializer(object_instance)
        data = serializer.data
        cliente = Cliente.objects.get(id=data.get("cliente"))
        cliente_serializer = ClienteSerializer(cliente, many=False)
        data.update({"cliente": cliente_serializer.data})
        return data

    def post(self, request, *args, **kwargs):
        serializer = GaranziaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManutenzioneListApiView(APIView):

    def get(self, request, *args, **kwargs):
        customers = Manutenzione.objects.all()
        res = []
        for customer in customers:
            res.append(self._get_response(customer))
        return Response(res, status=status.HTTP_200_OK)

    def _get_response(self, object_instance):
        serializer = ManutenzioneSerializer(object_instance)
        data = serializer.data
        cliente = Cliente.objects.get(id=data.get("cliente"))
        cliente_serializer = ClienteSerializer(cliente, many=False)
        data.update({"cliente": cliente_serializer.data})
        return data

    def post(self, request, *args, **kwargs):
        serializer = ManutenzioneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GaranziaDettaglioApiView(APIView):
    def _get_object(self, _id):
        try:
            return Garanzia.objects.get(id=_id)
        except Garanzia.DoesNotExist:
            return None

    def _get_response(self, object_instance):
        serializer = GaranziaSerializer(object_instance)
        data = serializer.data
        cliente = Cliente.objects.get(id=data.get("cliente"))
        cliente_serializer = ClienteSerializer(cliente, many=False)
        data.update({"cliente": cliente_serializer.data})
        return data

    def get(self, request, _id, *args, **kwargs):
        garanzia = self._get_object(_id)
        if not garanzia:
            return Response(
                {"res": "Garanzia non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = self._get_response(garanzia)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, _id):
        garanzia = self._get_object(_id)

        if not garanzia:
            return Response(
                {"res": "Garanzia non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GaranziaSerializer(garanzia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response("Parametri Errati", status.HTTP_400_BAD_REQUEST)

        data = self._get_response(garanzia)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, _id, format=None):
        try:
            garanzia = Garanzia.objects.get(id=_id)
            garanzia.delete()
            return Response({"res": "Garanzia eliminata con successo"}, status=status.HTTP_200_OK)

        except Garanzia.DoesNotExist:
            return Response(
                {"res": "Garanzia non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ManutenzioneDettaglioApiView(APIView):
    def _get_object(self, _id):
        try:
            return Manutenzione.objects.get(id=_id)
        except Manutenzione.DoesNotExist:
            return None

    def _get_response(self, object_instance):
        serializer = ManutenzioneSerializer(object_instance)
        data = serializer.data
        cliente = Cliente.objects.get(id=data.get("cliente"))
        cliente_serializer = ClienteSerializer(cliente, many=False)
        data.update({"cliente": cliente_serializer.data})
        return data

    def get(self, request, _id, *args, **kwargs):
        garanzia = self._get_object(_id)
        if not garanzia:
            return Response(
                {"res": "Garanzia non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = self._get_response(garanzia)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, _id):
        garanzia = self._get_object(_id)

        if not garanzia:
            return Response(
                {"res": "Garanzia non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ManutenzioneSerializer(garanzia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response("Parametri Errati", status.HTTP_400_BAD_REQUEST)

        data = self._get_response(garanzia)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, _id, format=None):
        try:
            garanzia = Manutenzione.objects.get(id=_id)
            garanzia.delete()
            return Response({"res": "Garanzia eliminata con successo"}, status=status.HTTP_200_OK)

        except Manutenzione.DoesNotExist:
            return Response(
                {"res": "Manutenzione non trovata"},
                status=status.HTTP_400_BAD_REQUEST
            )