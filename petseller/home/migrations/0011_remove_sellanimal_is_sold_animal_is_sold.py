# Generated by Django 4.1.7 on 2023-06-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_sellanimal_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellanimal',
            name='is_sold',
        ),
        migrations.AddField(
            model_name='animal',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
