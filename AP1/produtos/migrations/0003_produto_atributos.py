from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_categoria_produto_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='atributos',
            field=models.JSONField(blank=True, default=dict, help_text='Atributos variáveis do produto (marca, cor, RAM, etc.)'),
        ),
    ]