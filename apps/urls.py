from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from apps.views import ProductListView, UserProfileView, ProductDetailView, UserProfileUpdateView, get_districts, \
    MarketPageView, UrlsPageView, StatsPageView, RequestsPageView, CompetitionPageView, WithdrawPageView, \
    DiagramsPageView, CoinsPageView, AdminPageView, ProfilePageView, LikedProductView, OrderPageView, StreamCreateView

urlpatterns = [

    # auth

    path("login/", LoginView.as_view(
        template_name="apps/public-pages/login.html",
        next_page="main_page",
        redirect_authenticated_user=True
    ), name="login_page"),
    path("logout/", LogoutView.as_view(next_page="login_page"), name='logout'),
    path("user-update/", UserProfileUpdateView.as_view(), name='user_update'),
    path("settings/", UserProfileView.as_view(), name="settings_page"),
    path("profile/", ProfilePageView.as_view(), name="profile_page"),
    path('get-districts/', get_districts, name='get_districts'),

    # private

    path("market/", MarketPageView.as_view(), name="market_page"),
    path("urls/", UrlsPageView.as_view(), name="urls_page"),
    path("stats/", StatsPageView.as_view(), name="stats_page"),
    path("requests/", RequestsPageView.as_view(), name="requests_page"),
    path("competition/", CompetitionPageView.as_view(), name="competition_page"),
    path("withdraw/", WithdrawPageView.as_view(), name="withdraw_page"),
    path("diagrams/", DiagramsPageView.as_view(), name="diagrams_page"),
    path("coins/", CoinsPageView.as_view(), name="coins_page"),
    path("admin-page/", AdminPageView.as_view(), name="web_admin_page"),

    # public

    path("", ProductListView.as_view(), name="main_page"),
    path("product-detail/<int:pk>", ProductDetailView.as_view(), name="product_detail_page"),
    path("products/", ProductListView.as_view(template_name="apps/public-pages/products.html"), name="products_page"),
    path("orders/", OrderPageView.as_view(), name="orders_page"),
    path("liked-products/", LikedProductView.as_view(), name="liked_products_page"),
    path("not-found/", TemplateView.as_view(template_name="apps/not-found.html"), name="not-found_page"),

    path('create-stream/', StreamCreateView.as_view(), name='create-stream'),
]
