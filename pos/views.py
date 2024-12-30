from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Product, Sold, Cart, Customer

def checkout_view(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout_confirm_view(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer, created = Customer.objects.get_or_create(fullname=customer_name)

        cart_items = Cart.objects.all()
        for item in cart_items:
            Sold.objects.create(
                product=item.product,
                total_price=item.product.price * item.quantity,
                customer=customer
            )
        Cart.objects.all().delete()
        return redirect('checkout-success')

    return HttpResponse("Invalid request", status=400)

def checkout_success_view(request):
    return render(request, 'checkout_success.html')

def cart_view(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def cart_remove_view(request, item_pk):
    cart_item = get_object_or_404(Cart, pk=item_pk)
    cart_item.delete()
    return redirect('cart')

def cart_add_view(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product-list')

def cart_reset_view(request):
    Cart.objects.all().delete()
    return redirect('cart')

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'picture', 'description', 'stocks', 'category', 'price']
    success_url = '/'

def index(request):
    return render(request, 'POS.html')

def pos_view(request):
    products = Product.objects.all()
    cart_items = Cart.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'POS.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price})

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'picture', 'description', 'stocks', 'category', 'price']
    template_name = 'product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')
