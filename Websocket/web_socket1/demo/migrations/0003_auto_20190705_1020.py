# Generated by Django 2.2.3 on 2019-07-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20190705_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventinfo',
            name='type',
            field=models.IntegerField(default='1', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='eventinfo',
            name='name',
            field=models.CharField(default='null', max_length=30, null=True),
        ),
    ]
