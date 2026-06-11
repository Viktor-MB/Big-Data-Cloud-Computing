from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Produto, Pedido, ItemPedido
from .serializers import (
    CategoriaSerializer, ProdutoSerializer,
    PedidoSerializer, CriarPedidoSerializer, ItemPedidoSerializer
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria').all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['preco', 'data_criacao']

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.request.query_params.get('categoria')
        if categoria:
            qs = qs.filter(categoria__nome=categoria)

        preco_max = self.request.query_params.get('preco_max')
        if preco_max:
            qs = qs.filter(preco__lte=preco_max)

        # Filtros dentro do JSONField
        marca = self.request.query_params.get('marca')
        if marca:
            qs = qs.filter(atributos__marca__iexact=marca)

        cor = self.request.query_params.get('cor')
        if cor:
            qs = qs.filter(atributos__cor__iexact=cor)

        ram_gb = self.request.query_params.get('ram_gb')
        if ram_gb:
            qs = qs.filter(atributos__ram_gb=int(ram_gb))

        return qs

    @action(detail=False, methods=['get'], url_path='por-atributo')
    def por_atributo(self, request):
        chave = request.query_params.get('chave')
        valor = request.query_params.get('valor')
        if not chave or not valor:
            return Response({'erro': 'Forneça os parâmetros chave e valor.'}, status=400)
        qs = self.get_queryset().filter(**{f'atributos__{chave}__iexact': valor})
        return Response(self.get_serializer(qs, many=True).data)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.prefetch_related('itens__produto').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CriarPedidoSerializer
        return PedidoSerializer

    def create(self, request, *args, **kwargs):
        serializer = CriarPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pedido = serializer.save()
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='adicionar-item')
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()
        try:
            produto = Produto.objects.get(pk=request.data.get('produto'))
        except Produto.DoesNotExist:
            return Response({'erro': 'Produto não encontrado.'}, status=404)
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=int(request.data.get('quantidade', 1)),
            preco_unitario=produto.preco,
        )
        return Response(ItemPedidoSerializer(item).data, status=status.HTTP_201_CREATED)