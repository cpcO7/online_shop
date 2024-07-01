from django.db.models import CharField, Model, ForeignKey, CASCADE, ImageField, IntegerField, BigIntegerField, \
    PositiveIntegerField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import SlugBaseModel, TimeBaseModel


class Region(Model):
    title = CharField(max_length=100)

    def __str__(self):
        return self.title


class District(Model):
    title = CharField(max_length=100)
    region = ForeignKey("apps.Region", CASCADE, related_name="districts")

    def __str__(self):
        return self.title


class Category(SlugBaseModel):
    image = ImageField(upload_to="category/", null=True, blank=True)


class Product(TimeBaseModel, SlugBaseModel):
    image = ImageField(upload_to="product/")
    category = ForeignKey("apps.Category", CASCADE, related_name="products")
    price = PositiveIntegerField(db_default=0)
    benefit = PositiveIntegerField(db_default=0)
    description = CKEditor5Field()


class Stream(TimeBaseModel):
    title = CharField(max_length=255)
    count = IntegerField(db_default=1)
    product = ForeignKey("apps.Product", CASCADE, related_name="urls")
    user = ForeignKey("apps.User", CASCADE, related_name="urls")
    discount = BigIntegerField(db_default=0)
    benefit = PositiveIntegerField(db_default=0)
