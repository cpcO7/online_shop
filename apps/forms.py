from django.forms import ModelForm, ModelChoiceField, CharField, HiddenInput

from .models import User, Region, District, Stream, Product
from .models.order import Order
from .models.shop import Wishlist


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'district', 'address', 'telegram_id', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit and 'image' in self.cleaned_data:
            user.image = self.cleaned_data['image']

        if commit and 'banner' in self.cleaned_data:
            user.banner = self.cleaned_data['banner']

        user.save()
        return user


class StreamForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Stream
        fields = 'title', 'discount', 'product'

    def _save_m2m(self):
        super()._save_m2m()


class OrderCreateForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())
    stream = ModelChoiceField(queryset=Stream.objects.all(), required=False)

    class Meta:
        model = Order
        fields = "product", "phone_number", "name", "stream"


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = "__all__"


class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = 'quantity', 'district', 'location', 'send_order_date', 'description', "type"
