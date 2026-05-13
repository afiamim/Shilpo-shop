from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CartItem
from products_app.models import Product
from orders_app.models import Order

# Create your views here.
@login_required
def cart_view(request):

    if request.user.is_staff:
        messages.error(request, 'Admin accounts do not have a cart.')
        return redirect('product_list')

    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)

    return render(request, 'cart_app/cart.html', {'cart_items': cart_items,'total': total})
