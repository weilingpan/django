# Generated by Django 5.1 on 2024-12-01 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_process', '0002_alter_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
