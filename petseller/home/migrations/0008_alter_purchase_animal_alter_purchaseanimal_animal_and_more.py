# Generated by Django 4.1.6 on 2023-04-15 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_purchaseanimal_quantity_sellanimal_is_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_animal', to='home.animal'),
        ),
        migrations.AlterField(
            model_name='purchaseanimal',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.animal'),
        ),
        migrations.AlterField(
            model_name='sellanimal',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_animal', to='home.animal'),
        ),
    ]
