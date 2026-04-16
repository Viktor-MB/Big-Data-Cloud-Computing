from rest_framework import serializers
from .models import Categoria, Produto


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
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem', 'categoria', 'categoria_id', 'data_criacao']