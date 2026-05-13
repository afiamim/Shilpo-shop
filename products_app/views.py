from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm, CategoryForm

# Create your views here.

@login_required
def category_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can manage categories.')
        return redirect('product_list')
    categories = Category.objects.all()
    return render(request, 'products_app/category_list.html', {
        'categories': categories
    })


@login_required
def category_add(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can add categories.')
        return redirect('product_list')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'products_app/category_form.html', {'form': form})


@login_required
def category_edit(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can edit categories.')
        return redirect('product_list')
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products_app/category_form.html', {
        'form': form, 'category': category
    })


@login_required
def category_delete(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can delete categories.')
        return redirect('product_list')
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'products_app/category_delete.html', {
        'category': category
    })


def product_list(request):
    products   = Product.objects.all()
    categories = Category.objects.all()
    cat_id     = request.GET.get('category', '')
    if cat_id:
        products = products.filter(category_id=cat_id)
    return render(request, 'products_app/product_list.html', {
        'products':     products,
        'categories':   categories,
        'selected_cat': cat_id,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.review_set.all()
    return render(request, 'products_app/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })


@login_required
def product_add(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can add products.')
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products_app/product_form.html', {'form': form})


@login_required
def product_edit(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can edit products.')
        return redirect('product_list')
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products_app/product_form.html', {
        'form': form, 'product': product
    })


@login_required
def product_delete(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can delete products.')
        return redirect('product_list')
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product_list')
    return render(request, 'products_app/delete.html', {'product': product})
