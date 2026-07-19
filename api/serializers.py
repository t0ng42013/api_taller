from rest_framework import serializers
from .models import Cliente, Marca, Modelo, Vehiculo, TipoTrabajo, Repuesto, Trabajo, Pago, NivelDificultad

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class TrabajoSerializer(serializers.ModelSerializer):
    # Agregamos los campos calculados (@property) para que viajen en el JSON
    total_pagado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    deuda_pendiente = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    dias_en_deuda = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trabajo
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'