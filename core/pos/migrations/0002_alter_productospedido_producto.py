# Generated by Django 4.1.7 on 2023-04-07 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productospedido",
            name="producto",
            field=models.IntegerField(),
        ),
    ]
