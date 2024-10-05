from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .cart import Cart
from .forms import CartAddProductForm
from .models import Product

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)  # 5 minutes

# Product list view with pagination
# def product_list(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 10)  # Show 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'product_list.html', {'page_obj': page_obj})
def product_list(request):
    # Get the current page number
    page_number = request.GET.get('page', 1)

    # Try to get the cached page data based on the page number
    cache_key = f'product_list_page_{page_number}'
    page_obj = cache.get(cache_key)

    if not page_obj:
        # If not in cache, query the database
        products = Product.objects.all()
        paginator = Paginator(products, 10)  # Show 10 products per page
        page_obj = paginator.get_page(page_number)

        # Store the result in cache
        cache.set(cache_key, page_obj, timeout=CACHE_TTL)
    
    return render(request, 'product_list.html', {'page_obj': page_obj})

# Product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_add_product_form = CartAddProductForm()  # Create an instance of CartAddProductForm
    return render(request, 'product_detail.html', {'product': product, 'cart_add_product_form': cart_add_product_form})


# cart
# Add product to cart view
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart_detail')

# Remove product from cart view
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# Display cart detail view
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})