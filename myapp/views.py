from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Category, Products, Product_saved
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


def index(request):
    return render(request, 'myapp/index.html')


def legal(request):
    return render(request, 'myapp/legal.html')


def results(request, product_id):
    id = int(product_id)
    product_selected = get_object_or_404(Products, pk=id)
    category = get_object_or_404(Category, product__id=product_selected.id)
    # category = get_object_or_404(Category, pk=id)
    product_list = (category.product
                    .filter(nutriscore__lt=product_selected.nutriscore))
    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'paginate': True,
        'product_selected': product_selected
    }
    return render(request, 'myapp/results.html', context)


def product_detail(request, product_id):
    id = int(product_id)
    product_selected = get_object_or_404(Products, pk=id)
    context = {
        'product_selected': product_selected
    }
    return render(request, 'myapp/product_detail.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        product_list = Products.objects.all()
    else:
        product_list = Products.objects.filter(name__icontains=query)
    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # if len(categories) == 0:
    #     categories = Category.objects.filter(product__name__icontains=query)

    if len(products) == 0:
        raise Http404
    context = {
        'paginate': True,
        'products': products,
        'query': query
    }
    return render(request, 'myapp/search.html', context)


def user_products(request):
    user = request.user
    if user.is_authenticated:
        products_saved = Product_saved.objects.filter(user=user)
        context = {
            'products_saved': products_saved
        }
        return render(request, 'myapp/user_products.html', context)
    else:
        return redirect('login')


def save_product(request, product_selected_id, substitution_id):
    user = request.user
    if user.is_authenticated:
        product_selected = get_object_or_404(Products, pk=product_selected_id)
        substitution_product = get_object_or_404(Products, pk=substitution_id)
        Product_saved.objects.create(product_selected=product_selected,
                                     substitution_product=substitution_product,
                                     user=user)
        return redirect('user_products')
    else:
        return redirect('login')


def delete_product(request, product_id):
    user = request.user
    if user.is_authenticated:
        product_to_delete = get_object_or_404(Product_saved, pk=product_id)
        product_to_delete.delete()
        return redirect('user_products')
    else:
        return redirect('login')
