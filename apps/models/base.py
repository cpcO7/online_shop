from django.db.models import CharField, Model, DateTimeField, SlugField
from django.utils.text import slugify


class TimeBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    title = CharField(max_length=100)
    slug = SlugField(unique=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
