from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey, CASCADE, TextField, ImageField, TextChoices, BigIntegerField

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin', 'Admin'
        DRIVER = 'kuryer', 'Kuryer'
        USER = 'foydalanuvchi', 'Foydalanuvchi'

    image = ImageField(upload_to="user/", default="user/User-avatar.png")
    phone_number = CharField(max_length=50, unique=True)
    district = ForeignKey("apps.District", CASCADE, blank=True, null=True)
    bio = TextField(blank=True, null=True)
    telegram_id = CharField(max_length=50, blank=True, null=True)
    address = CharField(max_length=255, blank=True, null=True)
    type = CharField(max_length=20, choices=Type.choices, db_default=Type.USER)
    banner = ImageField(upload_to="banner/", default="banner/bg.avif")
    balance = BigIntegerField(db_default=0)

    # from_working_time = DateTimeField(blank=True, null=True)
    # to_working_time = DateTimeField(blank=True, null=True)
    # passport = DateTimeField(blank=True, null=True)

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
