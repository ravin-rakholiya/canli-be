# Generated by Django 3.2.4 on 2023-07-14 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practicetest', '0003_auto_20230713_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicetest',
            name='is_note',
            field=models.BooleanField(default=False),
        ),
    ]