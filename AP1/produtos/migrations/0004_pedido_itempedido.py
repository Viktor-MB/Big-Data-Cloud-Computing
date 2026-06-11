import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_produto_atributos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('pendente','Pendente'),('confirmado','Confirmado'),('cancelado','Cancelado'),('entregue','Entregue')],
                    default='pendente',
                    max_length=20,
                )),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('observacao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='produtos.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itens_pedido', to='produtos.produto')),
            ],
        ),
    ]