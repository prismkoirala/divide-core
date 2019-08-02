from django.urls import path
from .views import HomeView, ItemDetailView, CheckoutView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, add_to_cart_for_product, SizeView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product/<slug>/choose-size', SizeView.as_view(), name='item-size'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout_page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-product/<slug>/', add_to_cart_for_product, name='add-to-cart-product'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]
