# Generated by Django 3.1.3 on 2020-11-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(verbose_name='ID пользователя')),
                ('name', models.TextField(verbose_name='Имя пользователя')),
            ],
        ),
    ]
