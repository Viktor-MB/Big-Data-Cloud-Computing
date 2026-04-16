from django.urls import include, path
from .views import CategoriaViewSet, ProdutoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]