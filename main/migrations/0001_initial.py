# Generated by Django 3.0 on 2021-08-13 13:22

from django.db import migrations, models
import django.db.models.deletion
import main.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('user', models.EmailField(max_length=150)),
                ('contact_sum', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=150)),
                ('message_content', models.TextField(max_length=2000)),
                ('to', models.TextField()),
                ('sender_name', models.CharField(max_length=200)),
                ('message_status', models.CharField(max_length=50)),
                ('campaign_id', models.CharField(max_length=60)),
                ('campaign_name', models.CharField(blank=True, max_length=60, null=True)),
                ('scheduled_for', models.DateField(blank=True, null=True)),
                ('content', models.TextField(max_length=2000)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=150)),
                ('sender', models.CharField(max_length=100, unique=True)),
                ('company_name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=150)),
                ('title', models.CharField(max_length=100)),
                ('content_message', models.TextField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=150)),
                ('amount', models.IntegerField()),
                ('unit', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('tracking_code', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_numbers', models.TextField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.Group')),
=======
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_numbers', models.TextField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.group')),
>>>>>>> 104dbca0d1ff419d87ea8ed625f9430cc19aa1a8
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=250, verbose_name='first name')),
                ('last_name', models.CharField(max_length=250, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='phone')),
                ('address', models.CharField(max_length=250, null=True, verbose_name='address')),
                ('password', models.CharField(max_length=300, verbose_name='password')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('firebase_key', models.CharField(default='FBK', max_length=300, verbose_name='firebase_key')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', main.manager.UserManager()),
            ],
        ),
    ]
