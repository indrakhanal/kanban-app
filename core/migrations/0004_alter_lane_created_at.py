# Generated by Django 4.2.1 on 2023-05-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_kanbanboard_board_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lane',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
