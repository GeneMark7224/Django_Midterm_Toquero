from django.urls import path
from . import views
from .views import ProductCreateView, ProductListView, checkout_view, cart_view, cart_reset_view, cart_remove_view, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', views.index, name='pos-view'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('cart/reset/', cart_reset_view, name='cart-reset'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('cart/add/<int:product_pk>/', views.cart_add_view, name='cart-add'),
    path('cart/remove/<int:item_pk>/', cart_remove_view, name='cart-remove'),
    path('checkout/confirm/', views.checkout_confirm_view, name='checkout-confirm'),
    path('checkout/success/', views.checkout_success_view, name='checkout-success'),
    
    
]
