from django.db.models import TextChoices, ForeignKey, CASCADE, CharField

from apps.models import TimeBaseModel


class Order(TimeBaseModel):
    class Type(TextChoices):
        NEW = "yangi", "Yangi"
        ARCHIVE = "arxiv", "Arxiv"
        DELIVERING = "yetkazilmoqda", "Yetkazilmoqda"
        DELIVERED = "yetkazildi", "Yetkazildi"
        BROKEN = "nosoz_mahsulot", "Nosoz_mahsulot"
        RETURNED = "qaytib_keldi", "Qaytib_keldi"
        CANCELLED = "bekor_qilinfi", "Bekor_qilinfi"
        WAITING = "keyin_oladi", "Keyin_oladi"
        READY_TO_DELIVERY = "dastavkaga_tayyor", "Dastavkaga_tayyor"

    product = ForeignKey("apps.Product", CASCADE, related_name="orders")
    user = ForeignKey("apps.User", CASCADE, related_name="orders", null=True, blank=True)
    type = CharField(max_length=25, choices=Type.choices, db_default=Type.NEW)
