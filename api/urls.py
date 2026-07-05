from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from api.views import ClienteViewSet, PagoViewSet, TrabajoViewSet, VehiculoViewSet


router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'trabajos', TrabajoViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    # Si alguien entra a tu-web.com/api/login/, va a caer acá.
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
]