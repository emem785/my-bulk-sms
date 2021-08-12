# Generated by Django 3.2.4 on 2021-08-11 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2021-08-01 14:42:40+0000'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='ContactInit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=150)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_date_created', models.DateTimeField(auto_now=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.group')),
            ],
        ),
    ]
