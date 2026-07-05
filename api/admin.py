from django.contrib import admin
from .models import Cliente, Vehiculo, NivelDificultad, TipoTrabajo, Repuesto, Trabajo, Pago

# Personalizamos los textos del panel web
admin.site.site_header = 'Administración Mecánica Integral Alonso'
admin.site.site_title = 'Panel de Control'
admin.site.index_title = 'Gestión del Taller'

# Registramos los modelos de forma avanzada para ver columnas útiles

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Qué columnas mostrar en la lista
    list_display = ('nombre', 'telefono', 'cuit')
    # Agrega una barra de búsqueda por nombre o teléfono
    search_fields = ('nombre', 'telefono')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'cliente')
    # Permite buscar autos por patente o por el nombre del dueño
    search_fields = ('patente', 'cliente__nombre')
    # Agrega un filtro lateral por marca
    list_filter = ('marca',)

@admin.register(TipoTrabajo)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horas_estimadas', 'precio_base')
    search_fields = ('nombre',)

@admin.register(NivelDificultad)
class NivelDificultadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'multiplicador')

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'compatibilidad')
    search_fields = ('nombre', 'compatibilidad')
    # Filtro lateral para ver rápido los repuestos sin stock
    list_filter = ('cantidad',)

class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1  # Te muestra una fila vacía lista para cargar un pago nuevo

@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    # Usamos deuda_pendiente, que es la propiedad (@property) que creamos
    list_display = ('vehiculo', 'tipo_trabajo', 'fecha_ingreso', 'esta_pagado', 'deuda_pendiente')
    list_filter = ('fecha_ingreso',)
    search_fields = ('vehiculo__patente', 'vehiculo__cliente__nombre')

    # Le decimos que muestre la tabla de pagos al final de la pantalla
    inlines = [PagoInline]

    readonly_fields = ('precio_sugerido', 'deuda_pendiente')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('trabajo', 'monto', 'fecha_pago', 'metodo')
    list_filter = ('metodo', 'fecha_pago')