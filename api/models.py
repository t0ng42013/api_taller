import uuid
from django.contrib import admin
from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

class Cliente(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    cuit = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vehiculos")    
    anio = models.IntegerField(verbose_name="Año")
    patente = models.CharField(max_length=10, unique=True)

    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"

class NivelDificultad(models.Model):
    """Multiplicador de precio según lo complicado que sea el auto."""
    nombre = models.CharField(max_length=50)
    multiplicador = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} (x{self.multiplicador})"

class TipoTrabajo(models.Model):
    """Catálogo base de trabajos."""
    nombre = models.CharField(max_length=100) 
    horas_estimadas = models.DecimalField(max_digits=4, decimal_places=1) 
    precio_base = models.DecimalField(max_digits=10, decimal_places=2) 
    
    def __str__(self):
        return f"{self.nombre} (${self.precio_base})"

class Repuesto(models.Model):
    """Inventario interno del taller."""
    nombre = models.CharField(max_length=100) 
    compatibilidad = models.CharField(max_length=200, help_text="Ej: Peugeot 206, 207, Partner") 
    cantidad = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.nombre} - Stock: {self.cantidad}"
    
class Trabajo(models.Model):
    """La orden específica para un vehículo."""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="trabajos")
    kilometraje = models.IntegerField(help_text="Km del vehículo al ingresar", default=0)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.SET_NULL, null=True)
    dificultad = models.ForeignKey(NivelDificultad, on_delete=models.SET_NULL, null=True)
    
    horas_reales = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    
    recargo_mora = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    descripcion_adicional = models.TextField(blank=True, null=True) 
    
    repuestos_utilizados = models.ManyToManyField(Repuesto, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    @property
    def total_pagado(self):
        if not self.pk: 
            return Decimal('0.00')
        suma = self.pagos.aggregate(total=Sum('monto'))['total']
        return suma if suma else Decimal('0.00')
        
    @property
    def deuda_pendiente(self):
        precio = self.precio_final if self.precio_final else Decimal('0.00')
        recargo = self.recargo_mora if self.recargo_mora else Decimal('0.00')
        deuda = (precio + recargo) - self.total_pagado
        return deuda if deuda > 0 else Decimal('0.00')

    @property
    @admin.display(boolean=True, description='Pagado')
    def esta_pagado(self):
        return self.deuda_pendiente <= 0
        
    @property
    def dias_en_deuda(self):
        if self.deuda_pendiente > 0:
            return (timezone.now() - self.fecha_ingreso).days
        return 0

    @property
    @admin.display(description='Sugerencia Mano de Obra (Horas x Dificultad)')
    def precio_sugerido(self):
        VALOR_HORA = Decimal('20000.00') 
        if self.horas_reales:
            dificultad_mult = self.dificultad.multiplicador if self.dificultad else Decimal('1.00')
            return (Decimal(self.horas_reales) * VALOR_HORA) * dificultad_mult
        return Decimal('0.00')

    def __str__(self):
        return f"Trabajo en {self.vehiculo.patente}"

class Pago(models.Model):
    """Historial de entregas de dinero."""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=50, choices=[('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')])

    def __str__(self):
        return f"${self.monto} abonado el {self.fecha_pago.strftime('%d/%m/%Y')}"