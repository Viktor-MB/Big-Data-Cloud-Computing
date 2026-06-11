from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['preco_unitario']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'preco', 'categoria', 'data_criacao']
    list_filter = ['categoria']
    search_fields = ['nome', 'descricao']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'total', 'criado_em']
    list_filter = ['status']
    inlines = [ItemPedidoInline]


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'produto', 'quantidade', 'preco_unitario']