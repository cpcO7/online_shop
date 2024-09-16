from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView

from apps.forms import ProfileUpdateForm, StreamForm, OrderCreateForm, WishlistForm, OrderUpdateForm
from apps.models import Product, Category, User, District, Region, Stream, Order
from apps.models.shop import Wishlist


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "apps/private-pages/setting.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context


class ProductListView(ListView):
    queryset = Product.objects.order_by("id")
    template_name = "apps/public-pages/main-page.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('category')

        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        if category:
            qs = qs.filter(category__slug__contains=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "apps/public-pages/product-details.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self._cache_stream = None
        if pk is not None:
            self._cache_stream = get_object_or_404(Stream.objects.all(), pk=pk)
            self._cache_stream.views_count += 1
            self._cache_stream.save()
            return self._cache_stream.product
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        price = self.object.price
        if self._cache_stream:
            price -= self._cache_stream.discount

        ctx['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        ctx['price'] = price
        return ctx


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'apps/private-pages/setting.html'
    success_url = reverse_lazy('profile_page')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        if 'image' in self.request.FILES:
            user.image = self.request.FILES['image']

        if 'banner' in self.request.FILES:
            user.banner = self.request.FILES['banner']

        user.save()
        return super().form_valid(form)


def get_districts(request):
    region_id = request.GET.get('region_id')
    if region_id:
        districts = District.objects.filter(region_id=region_id).values('id', 'title')
        district_list = list(districts)
        return JsonResponse(district_list, safe=False)
    return JsonResponse([], safe=False)


class MarketPageView(LoginRequiredMixin, ProductListView):
    template_name = "apps/private-pages/market.html"


class StreamPageView(LoginRequiredMixin, ListView):
    queryset = Stream.objects.all()
    template_name = "apps/private-pages/stream.html"
    context_object_name = "streams"


class StatsPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/stats.html"


class RequestsPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/requests.html"


class CompetitionPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/competition.html"


class WithdrawPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/withdraw.html"


class DiagramsPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/diagrams.html"


class CoinsPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/coins.html"


class AdminPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/admin-page.html"


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/profile.html"


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = "apps/public-pages/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


class LikedProductView(LoginRequiredMixin, TemplateView):
    template_name = "apps/public-pages/liked-products.html"


class StreamCreateView(CreateView):
    template_name = 'apps/private-pages/market.html'
    form_class = StreamForm

    def form_valid(self, form):
        stream = form.save(commit=False)
        stream.user = self.request.user
        stream.save()
        return redirect("urls_page")

    def form_invalid(self, form):
        return super().form_invalid(form)


class SuccessOrderView(DetailView, CreateView):
    model = Product
    form_class = OrderCreateForm
    template_name = "apps/public-pages/success-order.html"

    def form_valid(self, form):
        stream = form.save(commit=False)
        if not self.request.user.is_anonymous:
            stream.user = self.request.user
        stream.save()
        return redirect(reverse("order_confirm_page", kwargs={"pk": stream.product.pk}))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class Error404(TemplateView):
    template_name = "apps/not-found.html"


class WishCreateDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        obj, created = Wishlist.objects.get_or_create(user=request.user, product_id=pk)
        if not created:
            obj.delete()
        return redirect('main_page')


class WishlistView(LoginRequiredMixin, ListView):
    queryset = Wishlist.objects.all()
    template_name = "apps/public-pages/wishlist.html"
    context_object_name = "wishes"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OperatorOrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = "apps/operator/order.html"
    context_object_name = "orders"


class OrderChangeView(LoginRequiredMixin, UpdateView, DetailView):
    queryset = Order.objects.all()
    form_class = OrderUpdateForm
    template_name = "apps/operator/change.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context
