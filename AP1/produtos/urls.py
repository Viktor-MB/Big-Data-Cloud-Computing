from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, PedidoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]