from django.db import models


class Categoria(models.Model):
    CATEGORIA_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('roupas', 'Roupas'),
        ('eletronicos', 'Eletrônicos'),
    ]

    nome = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        unique=True,
    )

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='produtos',
        blank=True,
        null=True,
    )
    atributos = models.JSONField(
        default=dict,
        blank=True,
        help_text='Atributos variáveis do produto (marca, cor, RAM, etc.)'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('entregue', 'Entregue'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    observacao = models.TextField(blank=True, null=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    def __str__(self):
        return f'Pedido #{self.pk} — {self.status}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido')
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido #{self.pedido.pk})'