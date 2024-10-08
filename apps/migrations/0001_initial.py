# Generated by Django 5.0.6 on 2024-07-15 11:19

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('image', models.ImageField(default='user/User-avatar.png', upload_to='user/')),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('telegram_id', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('operator', 'Operator'), ('manager', 'Manager'), ('admin', 'Admin'), ('kuryer', 'Kuryer'), ('foydalanuvchi', 'Foydalanuvchi'), ('yetkazib beruvchi', 'Yetkazib beruvchi')], db_default='foydalanuvchi', max_length=20)),
                ('banner', models.ImageField(default='banner/bg.avif', upload_to='banner/')),
                ('balance', models.BigIntegerField(db_default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.district')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('image', models.ImageField(upload_to='product/')),
                ('price', models.PositiveIntegerField(db_default=0)),
                ('benefit', models.PositiveIntegerField(db_default=0)),
                ('description', django_ckeditor_5.fields.CKEditor5Field()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='apps.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='apps.region'),
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('count', models.IntegerField(db_default=1)),
                ('discount', models.BigIntegerField(db_default=0)),
                ('views_count', models.IntegerField(db_default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='apps.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('yangi', 'Yangi'), ('arxiv', 'Arxiv'), ('yetkazilmoqda', 'Yetkazilmoqda'), ('yetkazildi', 'Yetkazildi'), ('nosoz_mahsulot', 'Nosoz_mahsulot'), ('qaytib_keldi', 'Qaytib_keldi'), ('bekor_qilinfi', 'Bekor_qilinfi'), ('keyin_oladi', 'Keyin_oladi'), ('dastavkaga_tayyor', 'Dastavkaga_tayyor')], db_default='yangi', max_length=25)),
                ('phone_number', models.CharField(max_length=50)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('send_order_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('courier', models.ForeignKey(blank=True, limit_choices_to={'type': 'yetkazib beruvchi'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courier', to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.district')),
                ('operator', models.ForeignKey(blank=True, limit_choices_to={'type': 'operator'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operator', to=settings.AUTH_USER_MODEL)),
                ('referral_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referral_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='apps.product')),
                ('stream', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='apps.stream')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='apps.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
