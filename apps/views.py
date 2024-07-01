from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView

from apps.forms import ProfileUpdateForm, StreamForm
from apps.models import Product, Category, User, District, Region, Stream


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "apps/private-pages/setting.html"
    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context


class ProductListView(ListView):
    queryset = Product.objects.order_by("id")
    template_name = "apps/public-pages/main-page.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.order_by("id")
        category = self.request.GET.get('category')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        if category:
            queryset = queryset.filter(category__slug__contains=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "apps/public-pages/product-details.html"


class UserProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'apps/private-pages/setting.html'
    success_url = reverse_lazy('profile_page')

    def get_object(self):
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


class UrlsPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/private-pages/urls.html"


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

    def get_login_url(self):
        return reverse_lazy('login_page')


class OrderPageView(LoginRequiredMixin, TemplateView):
    template_name = "apps/public-pages/orders.html"

    def get_login_url(self):
        return reverse_lazy('login_page')


class LikedProductView(LoginRequiredMixin, TemplateView):
    template_name = "apps/public-pages/liked-products.html"

    def get_login_url(self):
        return reverse_lazy('login_page')


class StreamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'apps/private-pages/market.html'
    form_class = StreamForm

    def form_valid(self, form):
        stream = form.save(commit=False)
        stream_user = self.request.user
        stream.save()
        return redirect("urls_page")

    def form_invalid(self, form):
        return super().form_invalid(form)


