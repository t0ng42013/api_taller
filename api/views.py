from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Cliente, Vehiculo, Trabajo, Pago, Marca, Modelo
from .serializers import ClienteSerializer, VehiculoSerializer, TrabajoSerializer, PagoSerializer, MarcaSerializer, ModeloSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class TrabajoViewSet(viewsets.ModelViewSet):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer

    @action(detail=False, methods=['get'])
    def deudores(self, request):
        # 1. Traemos de la base de datos todos los trabajos que no estén pagados
        trabajos_impagos = self.get_queryset().filter(pagado=False)
        
        # 2. Revisamos uno por uno para ver si realmente la deuda es mayor a cero
        lista_deudores = []
        for trabajo in trabajos_impagos:
            if trabajo.deuda_pendiente > 0:
                # Usamos tu serializer para convertir ese trabajo en JSON
                data_trabajo = self.get_serializer(trabajo).data
                lista_deudores.append(data_trabajo)
                
        # 3. Devolvemos la lista limpia al celular
        return Response(lista_deudores)

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all() 
    serializer_class = ModeloSerializer
    
    def get_queryset(self):
        # Empezamos con todos los modelos
        queryset = Modelo.objects.all()
        
        # Leemos si la URL trae un parámetro "?marca=X"
        marca_id = self.request.query_params.get('marca')
        
        # Si trae un ID de marca, filtramos la lista
        if marca_id is not None:
            queryset = queryset.filter(marca_id=marca_id)
            
        return queryset