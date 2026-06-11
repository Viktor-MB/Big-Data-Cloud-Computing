from rest_framework import serializers
from .models import Categoria, Produto, Pedido, ItemPedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem',
                  'categoria', 'categoria_id', 'atributos', 'data_criacao']


class ItemPedidoSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']
        read_only_fields = ['preco_unitario']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Pedido
        fields = ['id', 'status', 'observacao', 'itens', 'total', 'criado_em', 'atualizado_em']


class CriarPedidoSerializer(serializers.ModelSerializer):
    itens = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Pedido
        fields = ['status', 'observacao', 'itens']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item in itens_data:
            produto = Produto.objects.get(pk=item['produto'])
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item.get('quantidade', 1),
                preco_unitario=produto.preco,
            )
        return pedido