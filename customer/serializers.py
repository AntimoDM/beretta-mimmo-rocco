from rest_framework import serializers
from .models import Customer
from .models import Cliente
from .models import Intervento
from .models import TecnicoCaldaia
from .models import NumeroDiTelefonoAggiuntivo


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class InterventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervento
        fields = '__all__'


class TecnicoCaldaiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TecnicoCaldaia
        fields = '__all__'


class NumeroDiTelefonoAggiuntivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeroDiTelefonoAggiuntivo
        fields = '__all__'
