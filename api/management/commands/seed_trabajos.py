from django.core.management.base import BaseCommand
from api.models import TipoTrabajo, NivelDificultad

class Command(BaseCommand):
    help = 'Carga una lista inicial de tipos de trabajos y niveles de dificultad en la base de datos'

    def handle(self, *args, **kwargs):
        # 1. Cargar las dificultades base primero
        dificultades = [
            {"nombre": "Sencillo (Vehículo accesible)", "multiplicador": 1.00},
            {"nombre": "Normal (Estándar)", "multiplicador": 1.15},
            {"nombre": "Complicado (Poco espacio/Óxido)", "multiplicador": 1.35},
            {"nombre": "Alta Complejidad (Vehículo Alta Gama/Modificado)", "multiplicador": 1.60},
        ]

        self.stdout.write("Cargando Niveles de Dificultad...")
        for dif in dificultades:
            NivelDificultad.objects.get_or_create(
                nombre=dif["nombre"],
                defaults={"multiplicador": dif["multiplicador"]}
            )

        # 2. El listado completo de trabajos para taller general
        trabajos = [
            # Servicios Rápidos y Mantenimiento
            {"nombre": "Escaneo computarizado y borrado de fallas", "horas": 0.5, "precio": 15000.00},
            {"nombre": "Cambio de aceite y todos los filtros (Mano de obra)", "horas": 1.0, "precio": 20000.00},
            {"nombre": "Revisión general pre-VTV/ITV", "horas": 1.5, "precio": 30000.00},
            
            # Frenos
            {"nombre": "Cambio de pastillas de freno delanteras", "horas": 1.0, "precio": 25000.00},
            {"nombre": "Cambio de discos y pastillas delanteras", "horas": 2.0, "precio": 45000.00},
            {"nombre": "Cambio de cintas y campanas traseras", "horas": 2.5, "precio": 55000.00},
            {"nombre": "Purgado y cambio de líquido de frenos", "horas": 1.0, "precio": 20000.00},
            
            # Tren Delantero y Suspensión
            {"nombre": "Cambio de amortiguadores delanteros (Par)", "horas": 2.5, "precio": 60000.00},
            {"nombre": "Cambio de amortiguadores traseros (Par)", "horas": 1.5, "precio": 35000.00},
            {"nombre": "Cambio de bujes de parrilla (Tren delantero completo)", "horas": 4.5, "precio": 95000.00},
            {"nombre": "Cambio de rótulas y extremos de dirección", "horas": 2.0, "precio": 45000.00},
            {"nombre": "Cambio de homocinética / fuelle", "horas": 2.0, "precio": 45000.00},

            # Motor y Distribución
            {"nombre": "Cambio de kit de distribución (Correa y tensores)", "horas": 4.0, "precio": 90000.00},
            {"nombre": "Cambio de kit de distribución con bomba de agua", "horas": 5.0, "precio": 115000.00},
            {"nombre": "Cambio de correa poly-V / accesorios", "horas": 1.0, "precio": 20000.00},
            {"nombre": "Cambio de bujías y cables", "horas": 1.0, "precio": 20000.00},
            {"nombre": "Limpieza de inyectores y cuerpo mariposa", "horas": 3.0, "precio": 65000.00},
            {"nombre": "Cambio de bomba de nafta", "horas": 2.0, "precio": 45000.00},
            {"nombre": "Cambio de junta de tapa de cilindros", "horas": 12.0, "precio": 280000.00},
            {"nombre": "Extracción de motor para rectificadora", "horas": 15.0, "precio": 350000.00},

            # Transmisión y Embrague
            {"nombre": "Cambio de kit de embrague (Tracción delantera)", "horas": 7.0, "precio": 150000.00},
            {"nombre": "Cambio de kit de embrague (Tracción trasera/Camioneta)", "horas": 8.0, "precio": 180000.00},
            
            # Refrigeración
            {"nombre": "Cambio de radiador de agua", "horas": 2.0, "precio": 45000.00},
            {"nombre": "Limpieza de circuito de refrigeración y cambio de líquido", "horas": 2.0, "precio": 40000.00},
            {"nombre": "Cambio de termostato", "horas": 1.5, "precio": 30000.00},
        ]

        self.stdout.write("Cargando Catálogo de Trabajos...")
        for trabajo in trabajos:
            TipoTrabajo.objects.get_or_create(
                nombre=trabajo["nombre"],
                defaults={
                    "horas_estimadas": trabajo["horas"],
                    "precio_base": trabajo["precio"]
                }
            )

        self.stdout.write(self.style.SUCCESS('¡Seed completado! La base de datos ya tiene el tarifario listo.'))