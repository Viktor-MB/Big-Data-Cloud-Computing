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
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome