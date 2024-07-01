from django.forms import ModelForm, ModelChoiceField, CharField

from .models import User, Region, District, Stream, Product


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
        fields = ['title', 'discount', 'product', "benefit"]
